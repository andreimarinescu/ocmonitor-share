"""Live dashboard UI components for OpenCode Monitor."""

import os
import time
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.layout import Layout

from ..models.session import SessionData, TokenUsage


class DashboardUI:
    """UI components for the live dashboard."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize dashboard UI.

        Args:
            console: Rich console instance. If None, creates a new one.
        """
        self.console = console or Console()

    def create_header(self, session: SessionData) -> Panel:
        """Create header panel with session info."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header_text = f"""[bold blue]OpenCode Live Dashboard[/bold blue]
[cyan]Session:[/cyan] {session.session_id}
[cyan]Last Update:[/cyan] {current_time}
[cyan]Interactions:[/cyan] {session.interaction_count}"""

        return Panel(
            header_text,
            title="📊 Dashboard",
            title_align="left",
            border_style="blue"
        )

    def create_token_panel(self, session: SessionData, recent_file: Optional[Any] = None) -> Panel:
        """Create token consumption panel."""
        session_tokens = session.total_tokens

        # Recent interaction info
        recent_info = ""
        if recent_file:
            recent_info = f"""
[bold]Recent Interaction:[/bold]
  Input:      {recent_file.tokens.input:,}
  Output:     {recent_file.tokens.output:,}
  Cache W:    {recent_file.tokens.cache_write:,}
  Cache R:    {recent_file.tokens.cache_read:,}
"""

        token_text = f"""{recent_info}
[bold]Session Totals:[/bold]
  Input:      {session_tokens.input:,}
  Output:     {session_tokens.output:,}
  Cache W:    {session_tokens.cache_write:,}
  Cache R:    {session_tokens.cache_read:,}
  [bold blue]Total:      {session_tokens.total:,}[/bold blue]"""

        return Panel(
            token_text,
            title="🎯 Token Consumption",
            title_align="left",
            border_style="green"
        )

    def create_cost_panel(self, session: SessionData, pricing_data: Dict[str, Any],
                         quota: Optional[Decimal] = None) -> Panel:
        """Create cost tracking panel."""
        total_cost = session.calculate_total_cost(pricing_data)

        cost_text = f"[bold red]Session Cost: ${total_cost:.2f}[/bold red]\n"

        if quota:
            percentage = min(100, float(total_cost / quota) * 100)
            progress_bar = self.create_progress_bar(percentage)
            cost_color = self.get_cost_color(percentage)

            cost_text += f"[bold]Quota: ${quota:.2f}[/bold]\n"
            cost_text += f"[{cost_color}]{progress_bar}[/{cost_color}]"
        else:
            cost_text += "[dim]No quota configured[/dim]"

        return Panel(
            cost_text,
            title="💰 Cost Tracking",
            title_align="left",
            border_style="red"
        )

    def create_model_panel(self, session: SessionData, pricing_data: Dict[str, Any]) -> Panel:
        """Create model usage panel."""
        model_breakdown = session.get_model_breakdown(pricing_data)

        if not model_breakdown:
            return Panel("No model data", title="🤖 Models", border_style="yellow")

        model_lines = []
        for model, stats in model_breakdown.items():
            model_name = model[:20] + "..." if len(model) > 23 else model
            model_lines.append(
                f"[yellow]{model_name}[/yellow]: "
                f"{stats['tokens'].total:,} tokens, "
                f"${stats['cost']:.2f}"
            )

        model_text = "\n".join(model_lines)

        return Panel(
            model_text,
            title="🤖 Model Usage",
            title_align="left",
            border_style="yellow"
        )

    def create_context_panel(self, recent_file: Optional[Any],
                           context_window: int = 200000) -> Panel:
        """Create context window status panel."""
        if not recent_file:
            return Panel(
                "No recent interaction",
                title="🧠 Context Window",
                border_style="purple"
            )

        # Calculate context size (input + cache read + cache write from most recent)
        context_size = (recent_file.tokens.input +
                       recent_file.tokens.cache_read +
                       recent_file.tokens.cache_write)

        percentage = min(100, (context_size / context_window) * 100)
        progress_bar = self.create_progress_bar(percentage)
        context_color = self.get_context_color(percentage)

        context_text = f"""[bold]Current Size:[/bold] {context_size:,} tokens
[bold]Window Size:[/bold] {context_window:,} tokens
[{context_color}]{progress_bar}[/{context_color}]"""

        return Panel(
            context_text,
            title="🧠 Context Window",
            title_align="left",
            border_style="purple"
        )

    def create_burn_rate_panel(self, burn_rate: float) -> Panel:
        """Create token burn rate panel."""
        if burn_rate == 0:
            burn_text = "[dim]No recent activity[/dim]"
        else:
            burn_text = f"[bold green]{burn_rate:,.0f} tokens/minute[/bold green]"

            # Add trend indicator
            if burn_rate > 10000:
                burn_text += " 🔥"
            elif burn_rate > 5000:
                burn_text += " ⚡"
            else:
                burn_text += " 📈"

        return Panel(
            burn_text,
            title="⚡ Token Burn Rate",
            title_align="left",
            border_style="cyan"
        )

    def create_recent_file_panel(self, recent_file: Optional[Any]) -> Panel:
        """Create recent file info panel."""
        if not recent_file:
            return Panel(
                "No recent files",
                title="📄 Recent Interaction",
                border_style="white"
            )

        file_text = f"""[bold]File:[/bold] {recent_file.file_name}
[bold]Model:[/bold] {recent_file.model_id}"""

        if recent_file.time_data and recent_file.time_data.duration_ms:
            duration = self.format_duration(recent_file.time_data.duration_ms)
            file_text += f"\n[bold]Duration:[/bold] {duration}"

        return Panel(
            file_text,
            title="📄 Recent Interaction",
            title_align="left",
            border_style="white"
        )

    def create_dashboard_layout(self, session: SessionData, recent_file: Optional[Any],
                              pricing_data: Dict[str, Any], burn_rate: float,
                              quota: Optional[Decimal] = None,
                              context_window: int = 200000) -> Layout:
        """Create the complete dashboard layout."""
        layout = Layout()

        # Create panels
        header = self.create_header(session)
        token_panel = self.create_token_panel(session, recent_file)
        cost_panel = self.create_cost_panel(session, pricing_data, quota)
        model_panel = self.create_model_panel(session, pricing_data)
        context_panel = self.create_context_panel(recent_file, context_window)
        burn_rate_panel = self.create_burn_rate_panel(burn_rate)
        recent_file_panel = self.create_recent_file_panel(recent_file)

        # Setup layout structure
        layout.split_column(
            Layout(header, size=5),
            Layout(name="main", ratio=1)
        )

        layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1)
        )

        layout["left"].split_column(
            token_panel,
            cost_panel,
            burn_rate_panel
        )

        layout["right"].split_column(
            model_panel,
            context_panel,
            recent_file_panel
        )

        return layout

    def create_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Create a text-based progress bar."""
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percentage:.1f}%"

    def get_cost_color(self, percentage: float) -> str:
        """Get color for cost based on percentage."""
        if percentage >= 90:
            return "red"
        elif percentage >= 75:
            return "yellow"
        elif percentage >= 50:
            return "orange"
        else:
            return "green"

    def get_context_color(self, percentage: float) -> str:
        """Get color for context window based on percentage."""
        if percentage >= 95:
            return "red"
        elif percentage >= 85:
            return "yellow"
        elif percentage >= 70:
            return "orange"
        else:
            return "green"

    def format_duration(self, milliseconds: int) -> str:
        """Format duration in milliseconds to readable format."""
        if milliseconds < 1000:
            return f"{milliseconds}ms"

        seconds = milliseconds / 1000
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_simple_table(self, data: Dict[str, Any]) -> Table:
        """Create a simple data table for fallback rendering."""
        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")

        for key, value in data.items():
            table.add_row(key, str(value))

        return table