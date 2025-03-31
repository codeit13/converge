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
import random
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
            filename = await self.publish_article(article_content)
            result["filename"] = filename
        return result

    async def stream(self, prompt: str):
        """Asynchronously process a prompt and stream responses via SSE."""
        if not self.agent:
            await self.initialize()

        # Send initial message
        yield self._sse_format("thinking", "Starting to process your request...")

        try:
            config = {"configurable": {"thread_id": "1"}}
            inputs = {"messages": [("user", prompt)]}

            async for chunk in self.agent.astream(inputs, config, stream_mode="updates"):
                chunk = self._make_serializable(chunk)

                # if "output" in chunk:
                #     article_content = self.is_article_output(chunk["output"])
                #     if article_content:
                #         await self.publish_article(article_content)
                #     yield self._sse_format("chunk", chunk)

                if "agent" in chunk:
                    tool_names = self._extract_tool_names(chunk["agent"])
                    if tool_names:
                        thinking_msg = f"Calling {', '.join(tool_names)}..."
                        yield self._sse_format("thinking", thinking_msg)

                    content = chunk["agent"].get(
                        "messages", [])[0].get("content", "")
                    article_content = self.is_article_output(content)
                    if article_content:
                        filename = await self.publish_article(article_content)
                        chunk['agent']['messages'][0]['filename'] = filename
                    yield self._sse_format("chunk", chunk)

                else:
                    yield self._sse_format("chunk", chunk)

            # Send completion message
            yield self._sse_format("info", "Stream processing complete")

        except Exception as e:
            print(e)
            error_msg = f"Error in stream processing: {str(e)}"
            yield self._sse_format("error", error_msg)

    def _sse_format(self, event_type: str, chunk):
        """Helper function to format messages for SSE."""
        data = json.dumps({"type": event_type, "data": chunk})
        return f"data: {data}\n\n"

    def _extract_tool_names(self, agent_chunk):
        """Extract tool names from agent chunk."""
        tool_names = []
        messages = agent_chunk.get("messages", [])
        for message in messages:
            tool_calls = message.get(
                "additional_kwargs", {}).get("tool_calls", [])
            for tool_call in tool_calls:
                tool_name = tool_call.get("function", {}).get("name")
                if tool_name:
                    tool_names.append(tool_name)
        return tool_names

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
        foldername = f"article_{timestamp}"
        file_path = os.path.join(
            self.CONTENT_DIR, '/Posts/', foldername, 'index.md')

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Write the article content to the file.
                # Add front matter
                front_matter = f"""
                ---
                title: f"Blog #{random.randint(1, 1000)}"
                date: {datetime.now().strftime("%Y-%m-%d")}
                layout: "simple"
                ---
                """
                f.write(front_matter + article)
            print(f"Article published successfully at {file_path}")
            return filename
        except Exception as e:
            print(f"Error publishing article: {e}")
            return None

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
            result = {
                "type": obj.__class__.__name__,
                "content": obj.content,
            }

            for key in dir(obj):
                if not key.startswith("_") and key != "content":
                    result[key] = getattr(obj, key)
            return result
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
