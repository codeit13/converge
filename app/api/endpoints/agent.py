import asyncio
import os  # Added for robust path resolution
from services.agent_service import AgentService
from services.rag_service import FAISSRAGService
from models.run_history import Message as DBMessage, ChatSession
from utils.helpers import make_serializable
from datetime import datetime
from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, Request, HTTPException, UploadFile, File, Form
from uuid import uuid4
from typing import Annotated, Any, List, Optional, Union

router = APIRouter()

# Singleton RAG service instance (in-memory for now)
rag_service = FAISSRAGService()


class CreateChatRequest(BaseModel):
    user_id: str


class Message(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    message: str


class RunResponse(BaseModel):
    response: str


class StreamRequest(BaseModel):
    prompt: str
    chat_id: Optional[str] = None


class Tool(BaseModel):
    name: str
    description: str


class GetToolsResponse(BaseModel):
    tools: List[Tool]


class ChatSessionResponse(BaseModel):
    chat_id: str
    title: str
    last_message: Optional[str]
    created_at: datetime
    updated_at: datetime


class ChatMessageResponse(BaseModel):
    message_id: str
    role: str
    content: str
    timestamp: datetime
    metadata: dict[str, Any]


@router.post("/run", response_model=RunResponse)
async def run_agent(request: Request, query: RunRequest, user_id: Annotated[str | None, Header()] = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    agent_service: AgentService = request.app.state.agent_service
    agent_service.set_user_id(user_id)

    try:
        result = await agent_service.run(query.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    messages: List[AIMessage] = result.get("messages", [])

    # Convert messages to list of dicts for storage
    message_dicts = [
        {"role": msg.type, "content": msg.content}
        for msg in messages
    ]

    # Try to find existing session
    existing_session = await ChatSession.find_one({"session_id": user_id})

    if existing_session:
        # Append new messages to existing session
        existing_session.messages.extend(message_dicts)
        existing_session.timestamp = datetime.utcnow()
        await existing_session.save()
    else:
        # Create new session document
        run_doc = ChatSession(
            messages=message_dicts,
            agent_name=agent_service.agent_name,
            data={"query": query.message},
            timestamp=datetime.utcnow(),
            session_id=user_id
        )
        await run_doc.insert()

    return {"response": messages[-1].content if messages else ""}


@router.post("/stream")
async def stream_agent(
    request: Request,
    query: StreamRequest,
    user_id: Annotated[str | None, Header()] = None,
):
    """Stream agent responses"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    agent_service: AgentService = request.app.state.agent_service
    agent_service.set_user_id(user_id)

    try:
        print("Setting up streaming response")
        # Create human message for the agent
        human_message = HumanMessage(content=query.prompt)

        # Use the updated agent_service.stream method with chat_id for message capture
        response = StreamingResponse(
            agent_service.stream(human_message, chat_id=query.chat_id),
            media_type="text/event-stream"
        )
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"
        response.headers["X-Accel-Buffering"] = "no"  # Disable proxy buffering

        print("Streaming response setup complete")
        return response

    except Exception as e:
        error_msg = f"Error in stream setup: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/chats")
async def list_chats(user_id: Annotated[str | None, Header()] = None) -> List[ChatSessionResponse]:
    """Get all chat sessions for a user"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    # Find all active chat sessions for the user, sorted by updated_at
    sessions = await ChatSession.find(
        {"user_id": user_id, "is_active": True},
        sort=[("updated_at", -1)]
    ).to_list()

    return [
        ChatSessionResponse(
            chat_id=session.chat_id,
            title=session.title,
            last_message=session.messages[-1].content if session.messages else None,
            created_at=session.created_at,
            updated_at=session.updated_at
        ) for session in sessions
    ]


@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str, user_id: Annotated[str | None, Header()] = None) -> List[ChatMessageResponse]:
    """Get all messages in a chat session"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    # Find the chat session
    session = await ChatSession.find_one({"chat_id": chat_id, "user_id": user_id})
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    return [
        ChatMessageResponse(
            message_id=msg.message_id,
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp,
            metadata=msg.metadata
        ) for msg in session.messages
    ]


@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str, user_id: Annotated[str | None, Header()] = None):
    """Delete a chat session"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")

    # Find and delete the chat session
    session = await ChatSession.find_one({"chat_id": chat_id, "user_id": user_id})
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    await session.delete()
    return {"status": "success"}


@router.get("/history", response_model=List[ChatSession])
async def get_history():
    """Get all chat history"""
    return await ChatSession.find({"is_active": True}).sort([("updated_at", -1)]).to_list()


@router.get("/get-available-tools", response_model=GetToolsResponse)
async def get_tools(
    request: Request
):
    """
    An endpoint that returns a list of available tools.
    """
    agent_service: AgentService = request.app.state.agent_service
    try:
        tools = agent_service.get_tools()
        tools = [{"name": t.name, "description": t.description} for t in tools]
        tools.append({"name": "Reel Generator",
                     "description": "Generate a reel based on the given prompt"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"tools": tools}


@router.post("/chats", response_model=ChatSessionResponse)
async def create_chat(request: CreateChatRequest) -> ChatSessionResponse:
    """Create a new chat session."""
    # Log the incoming request for debugging
    print(f"Creating chat with request: {request}")

    user_id = request.user_id  # User ID is now part of request

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        # Create new chat session with empty messages
        chat_id = str(uuid4())
        chat_session = ChatSession(
            chat_id=chat_id,
            title="New Chat",
            messages=[],
            agent_name="Converge",  # Default agent name
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await chat_session.insert()
        print(f"Created new chat session with ID: {chat_id}")

        # Construct a valid response
        response = ChatSessionResponse(
            chat_id=chat_session.chat_id,
            title=chat_session.title,
            last_message=None,
            created_at=chat_session.created_at,
            updated_at=chat_session.updated_at
        )
        print(f"Returning response: {response}")
        return response
    except Exception as e:
        error_msg = f"Error creating chat session: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
