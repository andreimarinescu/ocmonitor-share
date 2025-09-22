"""Formatting utility functions for OpenCode Monitor."""

from decimal import Decimal
from typing import Any, Dict, List, Optional


class NumberFormatter:
    """Utility functions for number formatting."""

    @staticmethod
    def format_number(number: int) -> str:
        """Format numbers with thousands separators.

        Args:
            number: Number to format

        Returns:
            Formatted number string
        """
        return f"{number:,}"

    @staticmethod
    def format_currency(amount: Decimal, currency: str = "USD") -> str:
        """Format currency amounts.

        Args:
            amount: Amount to format
            currency: Currency code (currently only USD supported)

        Returns:
            Formatted currency string
        """
        if currency == "USD":
            return f"${amount:.4f}"
        else:
            return f"{amount:.4f} {currency}"

    @staticmethod
    def format_percentage(value: float, total: float, decimal_places: int = 1) -> str:
        """Format percentage values.

        Args:
            value: Numerator value
            total: Denominator value
            decimal_places: Number of decimal places

        Returns:
            Formatted percentage string
        """
        if total == 0:
            return "0.0%"

        percentage = (value / total) * 100
        return f"{percentage:.{decimal_places}f}%"

    @staticmethod
    def format_bytes(bytes_count: int) -> str:
        """Format byte counts in human-readable format.

        Args:
            bytes_count: Number of bytes

        Returns:
            Formatted byte string (e.g., "1.5 KB", "2.3 MB")
        """
        if bytes_count == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(bytes_count)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"

    @staticmethod
    def format_rate(value: float, unit: str = "per minute") -> str:
        """Format rate values.

        Args:
            value: Rate value
            unit: Unit description

        Returns:
            Formatted rate string
        """
        if value == 0:
            return f"0 {unit}"

        if value >= 1000000:
            return f"{value/1000000:.1f}M {unit}"
        elif value >= 1000:
            return f"{value/1000:.1f}K {unit}"
        else:
            return f"{value:.0f} {unit}"


class TableFormatter:
    """Utility functions for table formatting."""

    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length with suffix.

        Args:
            text: Text to truncate
            max_length: Maximum length including suffix
            suffix: Suffix to add if truncated

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        truncate_length = max_length - len(suffix)
        if truncate_length <= 0:
            return suffix[:max_length]

        return text[:truncate_length] + suffix

    @staticmethod
    def align_text(text: str, width: int, alignment: str = "left") -> str:
        """Align text within a given width.

        Args:
            text: Text to align
            width: Target width
            alignment: "left", "right", or "center"

        Returns:
            Aligned text
        """
        if len(text) >= width:
            return text

        if alignment == "left":
            return text.ljust(width)
        elif alignment == "right":
            return text.rjust(width)
        elif alignment == "center":
            return text.center(width)
        else:
            return text.ljust(width)

    @staticmethod
    def create_progress_bar(percentage: float, width: int = 20,
                          filled_char: str = "█", empty_char: str = "░") -> str:
        """Create a text-based progress bar.

        Args:
            percentage: Percentage (0-100)
            width: Width of the progress bar
            filled_char: Character for filled portion
            empty_char: Character for empty portion

        Returns:
            Progress bar string
        """
        filled = int(width * percentage / 100)
        bar = filled_char * filled + empty_char * (width - filled)
        return f"[{bar}] {percentage:.1f}%"


class ColorFormatter:
    """Utility functions for color formatting."""

    @staticmethod
    def get_cost_color(cost: Decimal, quota: Optional[Decimal] = None) -> str:
        """Get color for cost based on quota.

        Args:
            cost: Current cost
            quota: Optional quota to compare against

        Returns:
            Color name for Rich formatting
        """
        if quota is None:
            return "white"

        try:
            percentage = float(cost / quota) * 100
        except (ZeroDivisionError, TypeError, ValueError):
            return "white"

        if percentage >= 90:
            return "red"
        elif percentage >= 75:
            return "yellow"
        elif percentage >= 50:
            return "orange"
        else:
            return "green"

    @staticmethod
    def get_usage_color(current: int, maximum: int) -> str:
        """Get color for usage based on maximum.

        Args:
            current: Current usage
            maximum: Maximum allowed usage

        Returns:
            Color name for Rich formatting
        """
        if maximum == 0:
            return "white"

        percentage = (current / maximum) * 100

        if percentage >= 95:
            return "red"
        elif percentage >= 85:
            return "yellow"
        elif percentage >= 70:
            return "orange"
        else:
            return "green"

    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for status indicators.

        Args:
            status: Status string

        Returns:
            Color name for Rich formatting
        """
        status_colors = {
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "info": "blue",
            "active": "green",
            "inactive": "dim white",
            "pending": "yellow",
            "completed": "green",
            "failed": "red"
        }

        return status_colors.get(status.lower(), "white")


class DataFormatter:
    """Utility functions for data structure formatting."""

    @staticmethod
    def flatten_dict(data: Dict[str, Any], prefix: str = "", separator: str = ".") -> Dict[str, Any]:
        """Flatten a nested dictionary.

        Args:
            data: Dictionary to flatten
            prefix: Prefix for keys
            separator: Separator between nested keys

        Returns:
            Flattened dictionary
        """
        flattened = {}

        for key, value in data.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key

            if isinstance(value, dict):
                flattened.update(DataFormatter.flatten_dict(value, new_key, separator))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(DataFormatter.flatten_dict(item, f"{new_key}[{i}]", separator))
                    else:
                        flattened[f"{new_key}[{i}]"] = item
            else:
                flattened[new_key] = value

        return flattened

    @staticmethod
    def sanitize_for_csv(value: Any) -> str:
        """Sanitize a value for CSV export.

        Args:
            value: Value to sanitize

        Returns:
            Sanitized string value
        """
        if value is None:
            return ""

        # Convert to string
        str_value = str(value)

        # Escape quotes by doubling them
        str_value = str_value.replace('"', '""')

        # Wrap in quotes if contains comma, newline, or quote
        if ',' in str_value or '\n' in str_value or '"' in str_value:
            str_value = f'"{str_value}"'

        return str_value

    @staticmethod
    def format_model_name(model_name: str, max_length: int = 25) -> str:
        """Format model names for display.

        Args:
            model_name: Full model name
            max_length: Maximum display length

        Returns:
            Formatted model name
        """
        if len(model_name) <= max_length:
            return model_name

        # Try to keep important parts
        if "claude" in model_name.lower():
            # For Claude models, prioritize version info
            parts = model_name.split("-")
            if len(parts) >= 2:
                short_name = f"{parts[0]}-{parts[1]}"
                if len(short_name) <= max_length:
                    return short_name

        # Fallback to simple truncation
        return TableFormatter.truncate_text(model_name, max_length)