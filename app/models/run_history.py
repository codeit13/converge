from typing import Any, Optional
from beanie import Document, Indexed
from datetime import datetime
from pydantic import Field
from uuid import uuid4

class Message(Document):
    role: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_id: str = Field(default_factory=lambda: str(uuid4()))

    class Settings:
        name = "messages"

class ChatSession(Document):
    chat_id: Indexed(str) = Field(default_factory=lambda: str(uuid4()))
    title: str
    messages: list[Message]
    agent_name: str
    user_id: Indexed(str)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True

    class Settings:
        name = "chat_sessions"

    class Config:
        # Index chat_id and user_id for faster lookups
        indexes = [
            {"fields": ["chat_id"], "unique": True},
            {"fields": ["user_id"], "unique": False},
            {"fields": ["-updated_at"], "unique": False}  # For sorting by latest
        ]
