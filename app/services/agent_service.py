from datetime import datetime
import os
import traceback
from typing import Annotated, Any, AsyncGenerator, Dict, List, Optional
from uuid import uuid4
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from operator import add
from langchain_openai import ChatOpenAI
from langchain_community.tools import BraveSearch
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt.chat_agent_executor import AgentState
from pydantic import BaseModel
from services.tools.tools import generate_article
from config import settings
from models.run_history import Message as DBMessage, ChatSession
from utils.helpers import error_handler, extract_json_from_string, extract_tool_names, make_serializable, publish_article, sse_format
from utils.message_capture import create_user_message, create_assistant_message, save_messages_to_db, get_chat_messages

# Define some color codes for print statements
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m"
}


def merge_lists(a: List[dict], b: List[dict]) -> List[dict]: return [
    elem for pair in zip(a, b) for elem in pair]


class State(AgentState):
    messages: Annotated[List[AnyMessage], add_messages]
    articles: Annotated[List[dict[str, Any]], merge_lists]


class AgentService:
    def __init__(self):
        """
        Initialize the agent service.

        The agent is created using the ChatOpenAI model and the tools from the mcp_config.
        The mcp_config is a dictionary where the keys are the tool names and the values are
        the configurations for each tool.
        """

        self.agent_name = "Converge AI Assistant"
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.7, streaming=True)

        # Always resolve MCP server paths relative to this file to work in both local and Docker environments
        MCP_SERVERS_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../mcp-servers'))

        mcp_config = {
            "youtube": {
                "command": "node",
                "args": [os.path.join(MCP_SERVERS_BASE, "youtube/dist/index.js")],
                "transport": "stdio"
            },
            "sequential": {
                "command": "node",
                "args": [os.path.join(MCP_SERVERS_BASE, "sequential/dist/index.js")],
                "transport": "stdio"
            },
            # Add more tools as needed
        }

        filtered_config = {}
        for tool_name, config in mcp_config.items():
            file_path = config["args"][0]
            if os.path.exists(file_path):
                filtered_config[tool_name] = config
            else:
                print(
                    f"{COLORS['RED']}Tool {tool_name} not found at {file_path}{COLORS['RESET']}")

        self.mcp_config = filtered_config
        self.agent = None
        self.mcp_client = None

    @error_handler
    async def initialize(self):
        """
        Initialize the agent service.

        This method creates the MultiServerMCPClient and waits for the tools to be available.
        """
        print(f"{COLORS['BLUE']}Initializing agent service{COLORS['RESET']}")
        memory = MemorySaver()
        self.mcp_client = MultiServerMCPClient(self.mcp_config)
        try:
            await self.mcp_client.__aenter__()
            print(
                f"{COLORS['GREEN']}MCP client initialized successfully{COLORS['RESET']}")
        except Exception as e:
            print(
                f"{COLORS['RED']}Error entering MCP client context: {e}{COLORS['RESET']}")
            raise

        # Create the output parser and get JSON instructions.
        # output_parser = PydanticOutputParser(pydantic_object=ResponseFormat)
        # json_instructions = output_parser.get_format_instructions()

        prompt = f"""
            You are an advanced technical assistant with expert knowledge in programming, AI, and technology. Your task is to solve problems and answer questions using a sequential thinking approach while leveraging available tools.

Your first step will be to thoroughly ANALYZE the user query to identify the core problem and required information. After that, you will need to PLAN your approach by breaking down complex tasks into smaller, sequential steps. Make sure to IDENTIFY which tools are most appropriate for each step of your plan and EXECUTE each step methodically, using the right tool for each specific subtask. It's essential to VERIFY your intermediate results before proceeding to the next step and SYNTHESIZE all information into a coherent, accurate response.

When using tools, utilize them deliberately and with clear purpose.
Provide explicit reasoning for each tool selection.
If you encounter information that you don't know, please leverage your available tools.
For the latest information on any topic, consider using the search tool, and always construct specific queries rather than vague ones.
While executing code, validate inputs and expected outputs before running anything.
If you're uncertain about a fact, verify using the appropriate tools before responding and return tool responses as they are without additional formatting.

If you're asked to generate an article, do not provide an exact article or its summary; instead, restructure the information provided by the tool if it has already given the same info.
If a tool has provided an article link, inform the user that their article has been published at {{article_link}} and always return the article link at the end of your response.
Beautify the article link text in markdown.

Please analyze the following user query and proceed with your task:  

            ** Metadata **
            Current Date: {datetime.now().strftime("%Y-%m-%d")}
            Current Time: {datetime.now().strftime("%H:%M:%S")}
        """

        tools = self.mcp_client.get_tools()

        # Custom Tools
        # search_tool = BraveSearch.from_api_key(
        #     api_key=settings.BRAVE_SEARCH_API_KEY, search_kwargs={"count": 3})
        search_tool = TavilySearch(
            tavily_api_key=settings.TAVILY_SEARCH_API_KEY, max_results=2,
            topic="general",
        )

        article_generator_tool = generate_article

        tools.extend([search_tool, article_generator_tool])

        self.tools = tools

        self.agent = create_react_agent(
            state_schema=State,
            prompt=prompt,
            model=self.llm,
            tools=tools,
            checkpointer=memory,
        )
        # output_parser=output_parser

    @error_handler
    def set_user_id(self, user_id):
        self.user_id = user_id

    @error_handler
    def get_tools(self):
        return self.tools

    @error_handler
    async def stream(self, message: HumanMessage, chat_id: str = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream responses from the agent and capture messages for database storage"""
        print(
            f"{COLORS['CYAN']}Streaming response for message: {message.content[:30]}...{COLORS['RESET']}")

        # For message capture
        all_messages = []

        try:
            # Initialize agent if not already initialized
            if not self.agent:
                print(
                    f"{COLORS['YELLOW']}Agent not initialized, initializing now{COLORS['RESET']}")
                await self.initialize()

            # Create config with thread_id (using chat_id)
            config = {"configurable": {
                "thread_id": chat_id}} if chat_id else {}

            # Create and capture user message
            user_db_message = create_user_message(message.content)
            all_messages.append(user_db_message)

            # Prepare initial state and inputs
            # Clearing previously generated article in agent state, if any
            state_values = {}
            inputs = {"messages": [("user", message.content)]}

            # Stream responses
            try:
                # Check if agent state exists and messages are empty
                current_state = self.agent.get_state(config)
                if not current_state.values.get('messages', []) and chat_id:
                    # Load chat history if available
                    agent_messages, result = await get_chat_messages(chat_id, self.user_id)

                    if result["success"]:
                        print(
                            f"{COLORS['GREEN']}Loaded {result['message_count']} messages from chat_id: {chat_id}{COLORS['RESET']}")
                        state_values["messages"] = agent_messages
                    elif result["error"]:
                        print(
                            f"{COLORS['RED']}Error loading messages: {result['error']}{COLORS['RESET']}")
                    else:
                        print(
                            f"{COLORS['YELLOW']}No existing messages found for chat_id: {chat_id}{COLORS['RESET']}")

                # Update agent state
                self.agent.update_state(config, values=state_values)

                # Start streaming
                stream_generator = self.agent.astream(
                    inputs, config, stream_mode="updates")
                async for chunk in stream_generator:
                    chunk = make_serializable(chunk)

                    if "output" in chunk:
                        # Capture output message
                        try:
                            assistant_message = create_assistant_message({
                                "content": chunk.get("output", ""),
                                "metadata": {
                                    "role": "assistant",
                                    "timestamp": datetime.utcnow().isoformat()
                                }
                            })
                            all_messages.append(assistant_message)
                        except Exception as msg_error:
                            print(
                                f"{COLORS['RED']}Error creating output message: {msg_error}{COLORS['RESET']}")

                        yield sse_format("output", {'output': chunk['output'], 'existing_state': existing_state})
                    elif "agent" in chunk:
                        # Handle agent reasoning/tool calls
                        tool_names = extract_tool_names(chunk["agent"])
                        if tool_names:
                            yield sse_format("tool_calls", tool_names)

                        content = chunk["agent"].get(
                            "messages", [])[-1].get("content", None)

                        # Capture agent message if it has content
                        if content:
                            try:
                                assistant_message = create_assistant_message({
                                    "content": content,
                                    "metadata": {
                                        "role": "assistant",
                                        "type": "reasoning",
                                        "timestamp": datetime.utcnow().isoformat()
                                    }
                                })
                                all_messages.append(assistant_message)
                            except Exception as msg_error:
                                print(
                                    f"{COLORS['RED']}Error creating agent message: {msg_error}{COLORS['RESET']}")

                        yield sse_format("chunk", content)

                    else:
                        if 'tools' in chunk:
                            yield sse_format("tool_messages", chunk['tools'])
                        else:
                            yield sse_format("chunk", chunk)

            except GeneratorExit:
                print(
                    f"{COLORS['YELLOW']}Stream closed by client{COLORS['RESET']}")
                # Try to save messages even if client disconnected
                await save_messages_to_db(
                    user_id=self.user_id,  # Use the class variable user_id
                    chat_id=chat_id,
                    prompt=message.content,
                    messages=all_messages,
                    agent_name=self.agent_name
                )
                return
            except Exception as stream_error:
                print(
                    f"{COLORS['RED']}Error during stream generation: {stream_error}{COLORS['RESET']}")
                raise

            # Send completion message
            try:
                existing_state = self.agent.get_state(config).values
                existing_state = make_serializable(existing_state)
                yield sse_format("complete", existing_state)
            except Exception as state_error:
                print(
                    f"{COLORS['RED']}Error getting/sending state: {state_error}{COLORS['RESET']}")

            # Save messages to database at the end of the stream
            try:
                await save_messages_to_db(
                    user_id=self.user_id,  # Use the class variable user_id
                    chat_id=chat_id,
                    prompt=message.content,
                    messages=all_messages,
                    agent_name=self.agent_name
                )
            except Exception as db_error:
                print(
                    f"{COLORS['RED']}Error saving messages to database: {db_error}{COLORS['RESET']}")

        except Exception as e:
            print(
                f"{COLORS['RED']}Unhandled exception in stream method: {e}{COLORS['RESET']}")
            error_msg = f"Error in stream processing: {str(e)}"
            yield sse_format("error", error_msg)

    @error_handler
    async def run(self, messages: list, chat_id: str = None) -> dict:
        """
        Run the agent with the given messages.

        If the agent is not initialized, it will be initialized first.
        Checks if the final output contains an article block and calls publish_article if so.

        Args:
            messages: The user message as a string or list
            chat_id: Optional chat ID to load history from
        """
        if not self.agent:
            await self.initialize()

        # Prepare configuration
        config = {"configurable": {"thread_id": self.user_id}}
        state_values = {"article": {}}

        # Handle input messages formatting
        if isinstance(messages, str):
            user_input = messages
        elif isinstance(messages, list) and len(messages) > 0:
            user_input = messages[0] if isinstance(
                messages[0], str) else str(messages[0])
        else:
            user_input = ""

        inputs = {"messages": [("user", user_input)]}

        # Load chat history if available
        if chat_id:
            try:
                # Try to get chat history
                agent_messages, result = await get_chat_messages(chat_id, self.user_id)
                if result["success"] and agent_messages:
                    print(
                        f"{COLORS['GREEN']}Run: Loaded {result['message_count']} messages for context from chat_id: {chat_id}{COLORS['RESET']}")
                    state_values["messages"] = agent_messages
            except Exception as e:
                print(
                    f"{COLORS['RED']}Run: Error loading messages: {str(e)}{COLORS['RESET']}")

        # Update state and run agent
        self.agent.update_state(config, values=state_values)
        result = await self.agent.ainvoke(inputs, config)

        # Check if the output contains an article block
        response_text = result.get("response", "")
        res = extract_json_from_string(response_text)
        if res:
            articleSlug = await publish_article(self.CONTENT_DIR, res)
            result["articleSlug"] = articleSlug
        return result

    @error_handler
    async def shutdown(self):
        """Shutdown the agent service gracefully."""
        print(
            f"{COLORS['MAGENTA']}Shutting down agent service{COLORS['RESET']}")

        if self.mcp_client:
            try:
                # Instead of using __aexit__ directly, use a safer approach
                # Set the client to None before attempting to exit
                client = self.mcp_client
                self.mcp_client = None

                # Use a safer exit approach
                try:
                    await client.__aexit__(None, None, None)
                    print(
                        f"{COLORS['GREEN']}MCP client shutdown successfully{COLORS['RESET']}")
                except RuntimeError as re:
                    if "Attempted to exit cancel scope in a different task" in str(re):
                        # Just let it go - the event loop will clean up the resources
                        print(
                            f"{COLORS['YELLOW']}Handled cancel scope issue gracefully{COLORS['RESET']}")
                    else:
                        print(
                            f"{COLORS['RED']}Unexpected RuntimeError during shutdown: {re}{COLORS['RESET']}")
                except Exception as inner_e:
                    print(
                        f"{COLORS['RED']}Inner exception during shutdown: {inner_e}{COLORS['RESET']}")

            except RuntimeError as e:
                if "Attempted to exit cancel scope in a different task" in str(e):
                    print(
                        f"{COLORS['YELLOW']}Ignoring expected cancel scope task error{COLORS['RESET']}")
                else:
                    print(
                        f"{COLORS['RED']}Error during shutdown: {e}{COLORS['RESET']}")
            except Exception as e:
                print(
                    f"{COLORS['RED']}Exception during shutdown: {e}{COLORS['RESET']}")
        else:
            print(
                f"{COLORS['BLUE']}No MCP client to shutdown{COLORS['RESET']}")
