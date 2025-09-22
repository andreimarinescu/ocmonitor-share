"""Session data models for OpenCode Monitor."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
from decimal import Decimal
from pydantic import BaseModel, Field, computed_field, validator


class TokenUsage(BaseModel):
    """Model for token usage data."""
    input: int = Field(default=0, ge=0)
    output: int = Field(default=0, ge=0)
    cache_write: int = Field(default=0, ge=0)
    cache_read: int = Field(default=0, ge=0)

    @computed_field
    @property
    def total(self) -> int:
        """Calculate total tokens."""
        return self.input + self.output + self.cache_write + self.cache_read


class TimeData(BaseModel):
    """Model for timing information."""
    created: Optional[int] = Field(default=None, description="Creation timestamp in milliseconds")
    completed: Optional[int] = Field(default=None, description="Completion timestamp in milliseconds")

    @computed_field
    @property
    def duration_ms(self) -> Optional[int]:
        """Calculate duration in milliseconds."""
        if self.created is not None and self.completed is not None:
            return self.completed - self.created
        return None

    @computed_field
    @property
    def created_datetime(self) -> Optional[datetime]:
        """Get creation time as datetime object."""
        if self.created is not None:
            return datetime.fromtimestamp(self.created / 1000)
        return None

    @computed_field
    @property
    def completed_datetime(self) -> Optional[datetime]:
        """Get completion time as datetime object."""
        if self.completed is not None:
            return datetime.fromtimestamp(self.completed / 1000)
        return None


class InteractionFile(BaseModel):
    """Model for a single OpenCode interaction file."""
    file_path: Path
    session_id: str
    model_id: str = Field(default="unknown")
    tokens: TokenUsage = Field(default_factory=TokenUsage)
    time_data: Optional[TimeData] = Field(default=None)
    raw_data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    @validator('file_path')
    def validate_file_path(cls, v):
        """Ensure file path is a Path object."""
        return Path(v) if not isinstance(v, Path) else v

    @computed_field
    @property
    def file_name(self) -> str:
        """Get the file name."""
        return self.file_path.name

    @computed_field
    @property
    def modification_time(self) -> datetime:
        """Get file modification time."""
        return datetime.fromtimestamp(self.file_path.stat().st_mtime)

    def calculate_cost(self, pricing_data: Dict[str, Any]) -> Decimal:
        """Calculate cost for this interaction."""
        if self.model_id not in pricing_data:
            return Decimal('0.0')

        pricing = pricing_data[self.model_id]
        cost = Decimal('0.0')

        # Convert to cost per million tokens
        million = Decimal('1000000')

        cost += (Decimal(self.tokens.input) / million) * Decimal(str(pricing.input))
        cost += (Decimal(self.tokens.output) / million) * Decimal(str(pricing.output))
        cost += (Decimal(self.tokens.cache_write) / million) * Decimal(str(pricing.cache_write))
        cost += (Decimal(self.tokens.cache_read) / million) * Decimal(str(pricing.cache_read))

        return cost


class SessionData(BaseModel):
    """Model for a complete OpenCode session."""
    session_id: str
    session_path: Path
    files: List[InteractionFile] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @validator('session_path')
    def validate_session_path(cls, v):
        """Ensure session path is a Path object."""
        return Path(v) if not isinstance(v, Path) else v

    @computed_field
    @property
    def models_used(self) -> List[str]:
        """Get list of unique models used in this session."""
        return list(set(file.model_id for file in self.files))

    @computed_field
    @property
    def total_tokens(self) -> TokenUsage:
        """Calculate total token usage for the session."""
        total = TokenUsage()
        for file in self.files:
            total.input += file.tokens.input
            total.output += file.tokens.output
            total.cache_write += file.tokens.cache_write
            total.cache_read += file.tokens.cache_read
        return total

    @computed_field
    @property
    def start_time(self) -> Optional[datetime]:
        """Get session start time (earliest file creation time)."""
        times = [file.time_data.created_datetime for file in self.files
                if file.time_data and file.time_data.created_datetime]
        return min(times) if times else None

    @computed_field
    @property
    def end_time(self) -> Optional[datetime]:
        """Get session end time (latest file completion time)."""
        times = [file.time_data.completed_datetime for file in self.files
                if file.time_data and file.time_data.completed_datetime]
        return max(times) if times else None

    @computed_field
    @property
    def duration_ms(self) -> Optional[int]:
        """Calculate total session duration in milliseconds."""
        if self.start_time and self.end_time:
            return int((self.end_time - self.start_time).total_seconds() * 1000)
        return None

    @computed_field
    @property
    def total_processing_time_ms(self) -> int:
        """Calculate total processing time across all files."""
        total = 0
        for file in self.files:
            if file.time_data and file.time_data.duration_ms:
                total += file.time_data.duration_ms
        return total

    def calculate_total_cost(self, pricing_data: Dict[str, Any]) -> Decimal:
        """Calculate total cost for the session."""
        return sum(file.calculate_cost(pricing_data) for file in self.files)

    def get_model_breakdown(self, pricing_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Get breakdown of usage and cost by model."""
        breakdown = {}

        for model in self.models_used:
            model_files = [f for f in self.files if f.model_id == model]
            model_tokens = TokenUsage()
            model_cost = Decimal('0.0')

            for file in model_files:
                model_tokens.input += file.tokens.input
                model_tokens.output += file.tokens.output
                model_tokens.cache_write += file.tokens.cache_write
                model_tokens.cache_read += file.tokens.cache_read
                model_cost += file.calculate_cost(pricing_data)

            breakdown[model] = {
                'files': len(model_files),
                'tokens': model_tokens,
                'cost': model_cost
            }

        return breakdown

    @computed_field
    @property
    def interaction_count(self) -> int:
        """Get number of interactions (files) in this session."""
        return len(self.files)
    
    @property
    def non_zero_token_files(self) -> List[InteractionFile]:
        """Get files with non-zero token usage."""
        return [file for file in self.files if file.tokens.total > 0]