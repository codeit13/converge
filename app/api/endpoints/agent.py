from typing import List
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage
from pydantic import BaseModel
from datetime import datetime
from models.run_history import RunHistory
from services.agent_service import AgentService
import json
router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    message: str


class RunResponse(BaseModel):
    response: str


class StreamRequest(BaseModel):
    prompt: str


@router.post("/run", response_model=RunResponse)
async def run_agent(request: Request, query: RunRequest):
    agent_service: AgentService = request.app.state.agent_service
    try:
        result = await agent_service.run(query.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response_content = ""
    if result.get("messages"):
        response_content = result["messages"][-1].content
    run_doc = RunHistory(query=query.message,
                         response=response_content, timestamp=datetime.utcnow())
    await run_doc.insert()
    messages: List[AIMessage] = result.get("messages", [])

    return {"response": messages[-1].content if messages else ""}


@router.post("/stream")
async def stream_agent(request: Request, query: StreamRequest) -> StreamingResponse:
    print(request.headers)
    userid = request.headers.get("user_id")
    if not userid:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    print(f"Stream endpoint called with prompt: {query.prompt}")
    agent_service: AgentService = request.app.state.agent_service
    agent_service.set_user_id(userid)

    try:
        # Create a background task to save the history after streaming completes
        async def save_history():
            print("Background task: saving history for streamed response")
            # This is a placeholder - in a real implementation, you'd capture the final response
            # For now, we'll just save the query
            run_doc = RunHistory(
                query=query.prompt,
                response="Streamed response",
                timestamp=datetime.utcnow()
            )
            await run_doc.insert()
            print("History saved successfully")

        print("Setting up streaming response")
        # Return a streaming response with the agent's stream method
        response = StreamingResponse(
            agent_service.stream(query.prompt),
            media_type="text/event-stream",
            background=save_history
        )

        # Add CORS headers to ensure the stream works in the browser
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"
        response.headers["X-Accel-Buffering"] = "no"  # Disable proxy buffering

        print("Streaming response setup complete, returning to client")
        return response
    except Exception as e:
        error_msg = f"Error in stream_agent: {str(e)}"
        print(e)
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/history", response_model=list[RunHistory])
async def get_history():
    histories = await RunHistory.find_all().sort(-RunHistory.timestamp).to_list()
    return histories


@router.post("/test-stream")
async def test_stream():
    """
    A simple test endpoint that returns a streaming response.
    This is useful for debugging streaming issues without involving the agent.
    """
    print("Test stream endpoint called")

    async def generate_test_stream():
        # Send a few test messages with different types
        messages = [
            {"type": "thinking", "content": "This is a test thinking message"},
            {"type": "observation", "content": "This is a test observation"},
            {"type": "answer", "content": "This is a test answer"},
        ]

        # Send each message with a delay
        for i, msg in enumerate(messages):
            print(f"Sending test message {i+1}/{len(messages)}: {msg}")
            data = json.dumps(msg)
            yield f"data: {data}\n\n"
            await asyncio.sleep(1)  # Wait 1 second between messages

    response = StreamingResponse(
        generate_test_stream(),
        media_type="text/event-stream"
    )

    # Add CORS headers
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers["X-Accel-Buffering"] = "no"

    return response
