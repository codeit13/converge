"""
Agent service that uses langchain to interface with different models and tools.

The agent is created using the ChatOpenAI model and the tools from the mcp_config.
The mcp_config is a dictionary where the keys are the tool names and the values are
the configurations for each tool.

The service provides methods to run the agent and run a stream of messages.
"""

import asyncio
import json
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import settings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class AgentService:
    def __init__(self):
        """
        Initialize the agent service.

        The agent is created using the ChatOpenAI model and the tools from the mcp_config.
        The mcp_config is a dictionary where the keys are the tool names and the values are
        the configurations for each tool.
        """
        self.model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", streaming=True)

        self.mcp_config = {
            "youtube": {
                "command": "node",
                "args": ["mcp-servers/youtube/dist/index.js"],
                "transport": "stdio"
            },
            "sequential": {
                "command": "node",
                "args": ["mcp-servers/sequential/dist/index.js"],
                "transport": "stdio"
            },
            "twitter": {
                "command": "node",
                "args": ["mcp-servers/twitter/dist/index.js"],
                "transport": "stdio"
            }
        }
        self.agent = None
        self.mcp_client = None

    async def initialize(self):
        """
        Initialize the agent service.

        This method creates the MultiServerMCPClient and waits for the tools to be available.
        """
        memory = MemorySaver()
        self.mcp_client = MultiServerMCPClient(self.mcp_config)
        await self.mcp_client.__aenter__()

        tools = self.mcp_client.get_tools()
        self.agent = create_react_agent(self.model, tools, checkpointer=memory)

    async def run(self, messages: list) -> dict:
        """
        Run the agent with the given messages.

        If the agent is not initialized, it will be initialized first.
        """
        if not self.agent:
            await self.initialize()
        result = await self.agent.ainvoke({"messages": messages})
        return result

    async def stream(self, prompt: str):
        """
        Run the agent with the given messages and stream the response.

        If the agent is not initialized, it will be initialized first.
        Yields Server-Sent Events (SSE) formatted chunks for streaming to the frontend.
        """
        # print(f"Starting stream with prompt: {prompt}")

        if not self.agent:
            # print("Initializing agent for streaming")
            await self.initialize()

        # Send an initial message to confirm the stream is working
        initial_data = json.dumps(
            {"type": "thinking", "content": "Starting to process your request..."})
        # print(f"Sending initial message: {initial_data}")
        yield f"data: {initial_data}\n\n"

        try:
            # Simple counter for debugging
            chunk_count = 0
            config = {"configurable": {"thread_id": "1"}}
            inputs = {"messages": [("user", prompt)]}

            async for chunk in self.agent.astream(inputs, config, stream_mode="updates"):
                chunk_count += 1
                print(f"Received chunk {chunk_count}:", chunk)
                # Convert the chunk to a serializable format
                serializable_chunk = self._make_serializable(chunk)

                if "output" in chunk:
                    # Final answer from the agent
                    # print(f"Output found in chunk")
                    # Send the serialized chunk
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "agent" in chunk:
                    # Handle agent response format with messages
                    # print(f"Agent response found in chunk")
                    # Check if there are tool calls in the message
                    if chunk["agent"].get("messages") and len(chunk["agent"]["messages"]) > 0:
                        message = chunk["agent"]["messages"][0]

                        # Check for tool_calls in additional_kwargs
                        if hasattr(message, "additional_kwargs") and message.additional_kwargs.get("tool_calls"):
                            tool_calls = message.additional_kwargs["tool_calls"]
                            tool_names = []

                            # Extract tool names from tool_calls
                            for tool_call in tool_calls:
                                if "function" in tool_call and "name" in tool_call["function"]:
                                    tool_names.append(
                                        tool_call["function"]["name"])

                            # If we found tool names, send a thinking message
                            if tool_names:
                                thinking_msg = f"Calling {', '.join(tool_names)} {'tool' if len(tool_names) == 1 else 'tools'}..."
                                thinking_data = json.dumps(
                                    {"type": "thinking", "content": thinking_msg})
                                yield f"data: {thinking_data}\n\n"

                        # Check for tool_calls directly on the message
                        elif hasattr(message, "tool_calls") and message.tool_calls:
                            tool_names = [tool_call.get(
                                "name", "unknown tool") for tool_call in message.tool_calls]

                            # If we found tool names, send a thinking message
                            if tool_names:
                                thinking_msg = f"Calling {', '.join(tool_names)} {'tool' if len(tool_names) == 1 else 'tools'}..."
                                thinking_data = json.dumps(
                                    {"type": "thinking", "content": thinking_msg})
                                yield f"data: {thinking_data}\n\n"

                    # Send the serialized chunk
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "actions" in chunk:
                    # Agent is thinking or taking an action
                    # print(f"Actions found in chunk")
                    # Send the serialized chunk
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "steps" in chunk and chunk["steps"]:
                    # Results from tool execution
                    # print(f"Steps found in chunk")
                    # Send the serialized chunk
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"
                else:
                    # Unknown chunk type, send as is
                    # print(f"Unknown chunk type with keys: {list(chunk.keys())}")
                    # Send the serialized chunk
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

            # Send a completion message
            # print("Stream processing complete")
            completion_data = json.dumps(
                {"type": "info", "content": "Stream processing complete"})
            yield f"data: {completion_data}\n\n"

        except Exception as e:
            # Send error information to the client
            error_msg = f"Error in stream processing: {str(e)}"
            print(error_msg)
            error_data = json.dumps({"type": "error", "content": error_msg})
            yield f"data: {error_data}\n\n"

    def _make_serializable(self, obj):
        """Convert objects to JSON serializable format"""
        if isinstance(obj, (AIMessage, HumanMessage, SystemMessage)):
            # Handle LangChain message objects
            return {
                "type": obj.__class__.__name__,
                "content": obj.content,
                "additional_kwargs": obj.additional_kwargs
            }
        elif isinstance(obj, dict):
            # Process dictionary values recursively
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Process list items recursively
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, "__dict__"):
            # For other objects with __dict__, convert to dictionary
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):  # Skip private attributes
                    result[key] = self._make_serializable(value)
            return result
        else:
            # Return primitive types as is
            return obj

    async def shutdown(self):
        """Shutdown the agent service gracefully."""
        if self.mcp_client:
            try:
                # Use proper async context exit handling
                await self.mcp_client.__aexit__(None, None, None)
                print("MCP client shutdown successfully.")
            except Exception as e:
                print(f"Error during MCP shutdown: {e}")
