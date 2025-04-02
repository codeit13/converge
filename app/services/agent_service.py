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
from utils.helpers import error_handler, extract_json_from_string, extract_tool_names, make_serializable, publish_article, sse_format


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
        # self.CONTENT_DIR = os.path.join(
        #     os.path.dirname(os.getcwd()), "blog", "content")

        print(f"Content directory: {self.CONTENT_DIR}")

    @error_handler
    async def initialize(self):
        """
        Initialize the agent service.

        This method creates the MultiServerMCPClient and waits for the tools to be available.
        """
        memory = MemorySaver()
        self.mcp_client = MultiServerMCPClient(self.mcp_config)
        await self.mcp_client.__aenter__()

        prompt = """
        You are an expert SEO writer who creates markdown articles that rank #1 on Google. Follow these rules:  

        **SEO Guidelines:**  
        1. Include primary keyword in title + 1-2 secondary keywords  
        2. Use H2/H3 headings with keyword variations  
        3. Add meta description (155-160 chars)  
        4. Include 3-5 internal links and 2 authority external links  
        5. Use schema-ready FAQ section when relevant  

        **Content Structure Rules:**  
        1. Strict markdown formatting  
        2. Optional HTML only for:  
        - Complex tables  
        - Custom anchor links  
        - Schema markup (FAQ/HowTo)  
        3. Mobile-friendly layout:  
        - Short paragraphs (2-3 sentences)  
        - Bullet points for lists  
        - Bold/italic for key terms  

        **Response Format:**  
        When sharing the article, ALWAYS use this JSON structure:  
        {  
            "title": "SEO Title Here",  
            "article": "Full content in markdown...",  
            "articleSlug": "seo-friendly-url-slug",  
            "focusKeywords": ["primary", "secondary"],  
            "metaDescription": "Search-friendly snippet under 160 chars"  
        }  
        """

        tools = self.mcp_client.get_tools()
        self.agent = create_react_agent(
            prompt=prompt, model=self.model, tools=tools, checkpointer=memory)

    @error_handler
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
        article_data = extract_json_from_string(response_text)
        if article_data:
            articleSlug = await publish_article(self.CONTENT_DIR, article_data)
            result["articleSlug"] = articleSlug
        return result

    @error_handler
    async def stream(self, prompt: str):
        """Asynchronously process a prompt and stream responses via SSE."""
        if not self.agent:
            await self.initialize()

        # Send initial message
        yield sse_format("thinking", "Starting to process your request...")

        try:
            config = {"configurable": {"thread_id": "1"}}
            inputs = {"messages": [("user", prompt)]}

            async for chunk in self.agent.astream(inputs, config, stream_mode="updates"):
                # print("chunk: ", chunk)
                chunk = make_serializable(chunk)

                if "output" in chunk:
                    article_data = extract_json_from_string(chunk["output"])
                    if article_data:
                        articleSlug = await publish_article(self.CONTENT_DIR, article_data)
                        chunk['agent']['messages'][0]['articleSlug'] = articleSlug
                    yield sse_format("chunk", chunk)

                elif "agent" in chunk:
                    tool_names = extract_tool_names(chunk["agent"])
                    if tool_names:
                        thinking_msg = f"Calling {', '.join(tool_names)}..."
                        yield sse_format("thinking", thinking_msg)

                    content = chunk["agent"].get(
                        "messages", [])[0].get("content", "")
                    article_data = extract_json_from_string(content)
                    if article_data:
                        articleSlug = await publish_article(self.CONTENT_DIR, article_data)
                    yield sse_format("chunk", chunk)

                else:
                    yield sse_format("chunk", chunk)

            # Send completion message
            yield sse_format("info", "Stream processing complete")

        except Exception as e:
            print(e)
            error_msg = f"Error in stream processing: {str(e)}"
            yield sse_format("error", error_msg)

    @error_handler
    async def shutdown(self):
        """Shutdown the agent service gracefully."""
        if self.mcp_client:
            try:
                await self.mcp_client.__aexit__(None, None, None)
                print("MCP client shutdown successfully.")
            except Exception as e:
                print(f"Error during MCP shutdown: {e}")
