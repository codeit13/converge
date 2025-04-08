from datetime import datetime
import functools
import json
import os
import random
import re
import traceback
from typing import Callable, Optional, TypeVar, ParamSpec
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
def extract_json_from_string(llm_output: str) -> Optional[dict]:
    # print('***', llm_output, '***')
    def parse_json_candidate(json_str: str) -> Optional[dict]:
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Escape unescaped newline characters and try again.
            cleaned = re.sub(r'(?<!\\)\n', '\\n', json_str)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return None
    try:
        llm_output = llm_output.strip()

        # If the entire string is a JSON object.
        if llm_output.startswith('{') and llm_output.endswith('}'):
            result = parse_json_candidate(llm_output)
            if result is not None:
                return result

        # Look for JSON following a </think> tag.
        match = re.search(r'</think>\s*(\{.*\})', llm_output, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            result = parse_json_candidate(json_str)
            if result is not None:
                return result

        # Look for JSON inside triple backticks.
        match = re.search(r'```json(.*?)```', llm_output, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            result = parse_json_candidate(json_str)
            if result is not None:
                return result

        # Look for a JSON object anywhere in the string as a fallback.
        match = re.search(r'(\{.*\})', llm_output, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            result = parse_json_candidate(json_str)
            if result is not None:
                return result

        raise ValueError("No valid JSON found in the input string.")

    except Exception as e:
        return None


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


def sse_format(event_type: str, chunk):
    """Helper function to format messages for SSE."""
    data = json.dumps({"type": event_type, "data": chunk})
    return f"data: {data}\n\n"


@error_handler
def extract_tool_names(agent_chunk):
    """Extract tool names from agent chunk."""
    tool_names = []
    if 'messages' in agent_chunk:
        messages = agent_chunk['messages']
        for message in messages:
            if 'additional_kwargs' in message:
                if 'tool_calls' in message['additional_kwargs']:
                    tool_calls = message['additional_kwargs']['tool_calls']
                    for tool_call in tool_calls:
                        tool_name = tool_call['function']['name']
                        if tool_name:
                            tool_names.append(tool_name)
    return tool_names


def sanitize_title(title: str) -> str:
    """Remove or replace problematic characters in the title."""
    title = title.replace(":", " -")  # Replace ':' with ' -'
    # Remove problematic YAML characters
    title = re.sub(r'["\'|>#*]', '', title)
    return title.strip()


@error_handler
def publish_article(CONTENT_DIR, res: dict):
    """
    Publish the article extracted from the agent output.
    This method writes the article to a Markdown file in the content directory.
    """
    # Ensure the content directory exists
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)

    article_data = res
    if not article_data:
        return None

    # Ensure the 'Posts' directory exists
    article_folder_dir_name = article_data['slug'].lower()
    posts_dir = os.path.join(CONTENT_DIR, 'Posts', article_folder_dir_name)
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)

    file_path = os.path.join(posts_dir, 'index.md')

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            title = sanitize_title(article_data['title'])
            # Write the article content to the file.
            front_matter = f"""\n---\ntitle: {title}\ndate: {datetime.now().strftime("%Y-%m-%d")}\nslug: {article_data['slug']}\n---\n""".strip(
            )

            f.write(front_matter + "\n\n" + article_data['content'])
        print(f"Article published successfully at {file_path}")
        return f"http://localhost:1313/posts/{article_data['slug'].lower()}"
    except Exception as e:
        print(f"Error publishing article: {e}")
        return None


@error_handler
def is_article_output(text: str):
    """
    Extracts the article content from the given text enclosed by '---' or '##' markers.
    Returns the inner article content if found, otherwise returns None.
    """
    # Pattern to match content between '---' markers
    pattern_dashes = re.compile(r"---\s*(.*?)\s*---", re.DOTALL)
    match = pattern_dashes.search(text)
    if match:
        # Remove leading and trailing whitespaces and newlines
        return match.group(1).strip().strip('\n')

    # Pattern to match content between '##' markers
    pattern_sharp = re.compile(r"##\s*(.*?)\s*##", re.DOTALL)
    match = pattern_sharp.search(text)
    if match:
        return match.group(1).strip().strip('\n')

    return None


@error_handler
def make_serializable(obj):
    """Convert objects to JSON serializable format"""
    if callable(obj):
        return repr(obj)
    elif isinstance(obj, (AIMessage, HumanMessage, SystemMessage)):
        # Optionally adjust the type name (e.g., "AIMessage" -> "ai")
        type_name = obj.__class__.__name__
        if type_name.endswith("Message"):
            type_name = type_name[:-len("Message")].lower()
        result = {
            "type": type_name,
            "content": obj.content,
        }
        # Use __dict__ to iterate only over instance attributes
        for key, value in obj.__dict__.items():
            if not key.startswith("_") and key != "content":
                if callable(value):
                    result[key] = repr(value)
                else:
                    result[key] = make_serializable(value)
        return result
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                if callable(value):
                    result[key] = repr(value)
                else:
                    result[key] = make_serializable(value)
        return result
    else:
        return obj
