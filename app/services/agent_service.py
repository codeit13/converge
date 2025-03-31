"""
Agent service that uses langchain to interface with different models and tools.

The agent is created using the ChatOpenAI model and the tools from the mcp_config.
The mcp_config is a dictionary where the keys are the tool names and the values are
the configurations for each tool.

The service provides methods to run the agent and run a stream of messages.
"""

import asyncio
import json
import os
import re
from datetime import datetime
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

        # Define the directory where markdown files will be stored.
        # Ensure this path is correct relative to your FastAPI docker container.
        self.CONTENT_DIR = "/app/blog/content"

    async def initialize(self):
        """
        Initialize the agent service.

        This method creates the MultiServerMCPClient and waits for the tools to be available.
        """
        memory = MemorySaver()
        self.mcp_client = MultiServerMCPClient(self.mcp_config)
        await self.mcp_client.__aenter__()

        prompt = """You are an expert content writer with 10+years of experience in writing SEO ready articles, that rank in top 1st, 2nd article on google search index.
        """

        tools = self.mcp_client.get_tools()
        self.agent = create_react_agent(
            prompt=prompt, model=self.model, tools=tools, checkpointer=memory)

    async def run(self, messages: list) -> dict:
        """
        Run the agent with the given messages.

        If the agent is not initialized, it will be initialized first.
        Checks if the final output contains an article block and calls publish_article if so.
        """
        if not self.agent:
            await self.initialize()

        config = {"configurable": {"thread_id": "1"}}
        inputs = {"messages": [("user", messages)]}

        result = await self.agent.ainvoke(inputs, config)

        # Check if the output contains an article block
        response_text = result.get("response", "")
        article_content = self.is_article_output(response_text)
        if article_content:
            await self.publish_article(article_content)
        return result

    async def stream(self, prompt: str):
        """
        Run the agent with the given messages and stream the response.

        If the agent is not initialized, it will be initialized first.
        Yields Server-Sent Events (SSE) formatted chunks for streaming to the frontend.
        Checks for article output in streamed chunks and calls publish_article if found.
        """
        if not self.agent:
            await self.initialize()

        # Send an initial message to confirm the stream is working
        initial_data = json.dumps(
            {"type": "thinking", "content": "Starting to process your request..."})
        yield f"data: {initial_data}\n\n"

        published_article = False  # flag to ensure we publish only once per stream

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

                # Check for article markers if the chunk contains an "output" key
                if "output" in chunk:
                    article_content = self.is_article_output(chunk["output"])
                    if article_content and not published_article:
                        await self.publish_article(article_content)
                        published_article = True

                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "agent" in chunk:
                    # Handle potential tool calls in agent messages
                    if chunk["agent"].get("messages") and len(chunk["agent"]["messages"]) > 0:
                        message = chunk["agent"]["messages"][0]
                        if hasattr(message, "additional_kwargs") and message.additional_kwargs.get("tool_calls"):
                            tool_calls = message.additional_kwargs["tool_calls"]
                            tool_names = []
                            for tool_call in tool_calls:
                                if "function" in tool_call and "name" in tool_call["function"]:
                                    tool_names.append(
                                        tool_call["function"]["name"])
                            if tool_names:
                                thinking_msg = f"Calling {', '.join(tool_names)} {'tool' if len(tool_names) == 1 else 'tools'}..."
                                thinking_data = json.dumps(
                                    {"type": "thinking", "content": thinking_msg})
                                yield f"data: {thinking_data}\n\n"
                        elif hasattr(message, "tool_calls") and message.tool_calls:
                            tool_names = [tool_call.get(
                                "name", "unknown tool") for tool_call in message.tool_calls]
                            if tool_names:
                                thinking_msg = f"Calling {', '.join(tool_names)} {'tool' if len(tool_names) == 1 else 'tools'}..."
                                thinking_data = json.dumps(
                                    {"type": "thinking", "content": thinking_msg})
                                yield f"data: {thinking_data}\n\n"
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "actions" in chunk:
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

                elif "steps" in chunk and chunk["steps"]:
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"
                else:
                    data = json.dumps(
                        {"type": "chunk", "data": serializable_chunk})
                    yield f"data: {data}\n\n"

            # Send a completion message
            completion_data = json.dumps(
                {"type": "info", "content": "Stream processing complete"})
            yield f"data: {completion_data}\n\n"

        except Exception as e:
            error_msg = f"Error in stream processing: {str(e)}"
            print(error_msg)
            error_data = json.dumps({"type": "error", "content": error_msg})
            yield f"data: {error_data}\n\n"

    async def publish_article(self, article: str):
        """
        Publish the article extracted from the agent output.
        This method writes the article to a Markdown file in the content directory.
        """
        # Ensure the content directory exists
        if not os.path.exists(self.CONTENT_DIR):
            os.makedirs(self.CONTENT_DIR)

        # Generate a unique filename using the current UTC timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"article_{timestamp}.md"
        file_path = os.path.join(self.CONTENT_DIR, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Write the article content to the file.
                f.write(article)
            print(f"Article published successfully at {file_path}")
        except Exception as e:
            print(f"Error publishing article: {e}")

    def is_article_output(self, text: str):
        """
        Check if the given text contains an article block.
        Returns the inner article content if found, otherwise returns None.
        """
        print(type(text))
        pattern = re.compile(r"```article(.*?)```", re.DOTALL)
        match = pattern.search(text)
        if match:
            print("Article block found")
            return match.group(1).strip()

        print("No article block found")
        return None

    def _make_serializable(self, obj):
        """Convert objects to JSON serializable format"""
        if isinstance(obj, (AIMessage, HumanMessage, SystemMessage)):
            return {
                "type": obj.__class__.__name__,
                "content": obj.content,
                "additional_kwargs": obj.additional_kwargs
            }
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):
                    result[key] = self._make_serializable(value)
            return result
        else:
            return obj

    async def shutdown(self):
        """Shutdown the agent service gracefully."""
        if self.mcp_client:
            try:
                await self.mcp_client.__aexit__(None, None, None)
                print("MCP client shutdown successfully.")
            except Exception as e:
                print(f"Error during MCP shutdown: {e}")
