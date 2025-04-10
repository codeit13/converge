from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from uuid import uuid4

from models.run_history import Message as DBMessage, ChatSession


async def save_messages_to_db(
    user_id: str,
    chat_id: str,
    prompt: str,
    messages: List[DBMessage],
    agent_name: str
) -> None:
    """
    Save messages to the database.
    
    Args:
        user_id: The ID of the user
        chat_id: The ID of the chat session (if any)
        prompt: The initial prompt
        messages: The list of messages to save
        agent_name: The name of the agent
    """
    try:
        if chat_id:
            # Find existing chat session
            existing_session = await ChatSession.find_one(
                {"chat_id": chat_id, "user_id": user_id}
            )
            if not existing_session:
                print(f"Chat session not found: {chat_id}")
                return
            
            existing_session.messages.extend(messages)
            existing_session.updated_at = datetime.utcnow()
            await existing_session.save()
            print(f"Messages appended to existing chat session {existing_session.chat_id}")
        else:
            # Create new chat session
            title = prompt[:50] + "..." if len(prompt) > 50 else prompt
            chat_id = str(uuid4())
            chat_session = ChatSession(
                chat_id=chat_id,
                title=title,
                messages=messages,
                agent_name=agent_name,
                user_id=user_id,
                metadata={"initial_prompt": prompt},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            await chat_session.insert()
            print(f"New chat session created with ID {chat_session.chat_id}")
    except Exception as e:
        print(f"Error saving messages to database: {e}")


def create_user_message(prompt: str) -> DBMessage:
    """
    Create a user message object.
    
    Args:
        prompt: The user's prompt
        
    Returns:
        DBMessage: The user message object
    """
    return DBMessage(
        message_id=str(uuid4()),
        role="user",
        content=prompt,
        timestamp=datetime.utcnow(),
        metadata={}
    )


def create_assistant_message(chunk: Dict[str, Any]) -> DBMessage:
    """
    Create an assistant message from a chunk.
    
    Args:
        chunk: The chunk from the agent service
        
    Returns:
        DBMessage: The assistant message object
    """
    return DBMessage(
        message_id=str(uuid4()),
        role="assistant",
        content=chunk.get("content", ""),
        timestamp=datetime.utcnow(),
        metadata=chunk.get("metadata", {})
    )


async def get_chat_messages(chat_id: str, user_id: str) -> Tuple[List[Tuple[str, str]], Dict[str, Any]]:
    """
    Fetch messages for a chat session and convert them to agent format.
    
    Args:
        chat_id: The ID of the chat session
        user_id: The ID of the user
        
    Returns:
        Tuple containing:
        - List of (role, content) tuples for agent consumption
        - Dictionary with metadata like success status and message count
    """
    result = {
        "success": False,
        "message_count": 0,
        "error": None
    }
    
    try:
        if not chat_id or not user_id:
            return [], result
            
        # Find existing chat session
        existing_session = await ChatSession.find_one(
            {"chat_id": chat_id, "user_id": user_id}
        )
        
        if not existing_session or not existing_session.messages:
            return [], result
            
        # Convert DB messages to agent messages format
        agent_messages = []
        for msg in existing_session.messages:
            if msg.role == "user":
                agent_messages.append(("user", msg.content))
            elif msg.role == "assistant":
                agent_messages.append(("assistant", msg.content))
        
        result["success"] = True
        result["message_count"] = len(agent_messages)
        return agent_messages, result
        
    except Exception as e:
        result["error"] = str(e)
        return [], result
