from datetime import datetime
import os
from typing import Annotated, Any, List, Optional
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
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
from utils.helpers import error_handler, extract_json_from_string, extract_tool_names, make_serializable, publish_article, sse_format


class State(AgentState):
    messages: Annotated[List[AnyMessage], add_messages]
    article: dict[str, Any]


class AgentService:
    def __init__(self):
        """
        Initialize the agent service.

        The agent is created using the ChatOpenAI model and the tools from the mcp_config.
        The mcp_config is a dictionary where the keys are the tool names and the values are
        the configurations for each tool.
        """

        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.5, streaming=True)

        self.mcp_config = {
            # "youtube": {
            #     "command": "node",
            #     "args": ["mcp-servers/youtube/dist/index.js"],
            #     "transport": "stdio"
            # },
            "sequential": {
                "command": "node",
                "args": ["mcp-servers/sequential/dist/index.js"],
                "transport": "stdio"
            },
        }
        self.agent = None
        self.mcp_client = None

    @error_handler
    async def initialize(self):
        """
        Initialize the agent service.

        This method creates the MultiServerMCPClient and waits for the tools to be available.
        """
        memory = MemorySaver()
        self.mcp_client = MultiServerMCPClient(self.mcp_config)
        await self.mcp_client.__aenter__()

        # Create the output parser and get JSON instructions.
        # output_parser = PydanticOutputParser(pydantic_object=ResponseFormat)
        # json_instructions = output_parser.get_format_instructions()

        prompt = f"""
            You are an advanced technical assistant with expert knowledge in programming, AI, and technology. Your task is to solve problems and answer questions using a sequential thinking approach while leveraging available tools.

            ## Sequential Thinking Process
            1. ANALYZE the user query thoroughly to identify the core problem and required information
            2. PLAN your approach by breaking down complex tasks into smaller, sequential steps
            3. IDENTIFY which tools are most appropriate for each step of your plan
            4. EXECUTE each step methodically, using the right tool for each specific subtask
            5. VERIFY your intermediate results before proceeding to the next step
            6. SYNTHESIZE all information into a coherent, accurate response

            ## Tool Usage Guidelines
            - Use tools deliberately and with clear purpose.
            - Provide explicit reasoning for each tool selection.
            - If you don't know any information please try to use your available tools.
            - For latest information on any topic, use search tool.
            - When using the search tool, construct specific queries rather than vague ones.
            - For code execution, validate inputs and expected outputs before running.
            - When uncertain about a fact, use appropriate tools to verify before responding.
            - Return tool responses as it is without any additional formatting.

            ## Article Generation Guidelines (When Requested)
            - Don't provide exact article, if a tool have already provided the same info, you can simply refer to the info provided by the tool.

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
    async def run(self, messages: list) -> dict:
        """
        Run the agent with the given messages.

        If the agent is not initialized, it will be initialized first.
        Checks if the final output contains an article block and calls publish_article if so.
        """
        if not self.agent:
            await self.initialize()

        config = {"configurable": {"thread_id": self.user_id}}
        inputs = {"messages": [("user", messages)]}

        result = await self.agent.ainvoke(inputs, config)

        # Check if the output contains an article block
        response_text = result.get("response", "")
        res = extract_json_from_string(response_text)
        if res:
            articleSlug = await publish_article(self.CONTENT_DIR, res)
            result["articleSlug"] = articleSlug
        return result

    @error_handler
    async def stream(self, prompt: str):
        """Asynchronously process a prompt and stream responses via SSE."""
        if not self.agent:
            await self.initialize()

        # Send initial message
        # yield sse_format("thinking", "Reasoning...")

        try:
            config = {"configurable": {"thread_id": self.user_id}}
            inputs = {"messages": [("user", prompt)]}

            async for chunk in self.agent.astream(inputs, config, stream_mode="updates"):
                print("chunk: ", chunk)
                chunk = make_serializable(chunk)

                # print("chunk serialized: ", chunk)
                if "output" in chunk:
                    print(
                        "******************************* contains output *******************************")
                    existing_state = self.agent.get_state(config).values
                    yield sse_format("output", {'output': chunk['output'], 'existing_state': existing_state})

                elif "agent" in chunk:
                    # print("contains agent")
                    tool_names = extract_tool_names(chunk["agent"])
                    # print("tool names: ", tool_names)
                    if tool_names:
                        yield sse_format("tool_calls", tool_names)

                    content = chunk["agent"].get(
                        "messages", [])[-1].get("content", None)
                    # print("content: ", content)

                    yield sse_format("chunk", content)

                else:
                    # print("contains neither")
                    if 'tools' in chunk:
                        yield sse_format("tool_messages", chunk['tools'])
                    else:
                        yield sse_format("chunk", chunk)

            # Send completion message

            existing_state = self.agent.get_state(config).values
            existing_state = make_serializable(existing_state)
            yield sse_format("complete", existing_state)

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
