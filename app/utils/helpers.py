import functools
import traceback
from typing import Callable, TypeVar, ParamSpec
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

console = Console()

# Type variables for generic function typing
P = ParamSpec('P')  # For parameters
R = TypeVar('R')    # For return type


def error_handler(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that provides detailed error handling and tracing.

    Args:
        func: The function to wrap with error handling

    Returns:
        Wrapped function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            console.print(f"\n[red]{'='*50}[/red]")
            console.print(
                f"[red bold]Error in function:[/red bold] [yellow]{func.__name__}[/yellow]")
            console.print(
                f"[red bold]Error type:[/red bold] [yellow]{type(e).__name__}[/yellow]")
            console.print(
                f"[red bold]Error message:[/red bold] [yellow]{str(e)}[/yellow]")
            console.print("\n[red bold]Traceback:[/red bold]")
            console.print(f"[yellow]{traceback.format_exc()}[/yellow]")
            console.print(f"[red]{'='*50}[/red]\n")
            raise
    return wrapper


@error_handler
def pretty_print_messages(messages):
    """Pretty print messages for debugging"""
    table = Table(
        show_header=True,
        header_style="bold white",
        style="blue",
        row_styles=["green", "green"],
        border_style="white"
    )
    table.add_column("Role")
    table.add_column("Content")
    table.add_column("Tokens (I/O)")

    for msg in messages:
        role = msg.__class__.__name__

        if not msg.content:
            if hasattr(msg, 'tool_calls'):
                content = 'Call these tools: ' + \
                    ', '.join([tc['name'] for tc in msg.tool_calls])
            else:
                content = 'N/A'
        else:
            content = msg.content

        total_tokens = msg.response_metadata.get(
            'token_usage', {}).get('total_tokens', 'N/A')

        table.add_row(
            role,
            content,
            str(total_tokens)
        )

    console.print(Panel(table, title="Prompt to LLM"))
