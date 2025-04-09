import asyncio
from fastapi import APIRouter, Header, HTTPException
from typing import Annotated, List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from models.run_history import ChatSession, Message
from pymongo import DESCENDING
import random

router = APIRouter()

class TimeRange(BaseModel):
    """Time range for analytics queries"""
    days: int = 30

class AnalyticsSummary(BaseModel):
    """Summary statistics for the dashboard"""
    total_chats: int
    total_messages: int
    avg_messages_per_chat: float
    active_users: int
    completion_rate: float
    recent_activity: List[Dict[str, Any]]
    chat_trend: List[Dict[str, Any]]
    message_types: Dict[str, int]

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    time_range: TimeRange = TimeRange(),
    user_id: Annotated[str | None, Header()] = None
):
    """Get analytics summary for the dashboard"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=time_range.days)
    
    # Query all chats for this user within the time range
    query = {
        "user_id": user_id,
        "created_at": {"$gte": start_date, "$lte": end_date}
    }
    
    # Get chat sessions
    # Make sure to await the find and sort operations
    chat_cursor = ChatSession.find(query).sort([("created_at", DESCENDING)])
    all_chats = await chat_cursor.to_list()
    
    # Get all messages for these chats
    total_messages = 0
    user_messages = 0
    ai_messages = 0
    message_dates = {}
    
    for chat in all_chats:
        # Safely handle message counting
        if hasattr(chat, 'messages') and chat.messages:
            total_messages += len(chat.messages)
            
            for msg in chat.messages:
                # Count message types
                if isinstance(msg, dict):
                    if msg.get("role") == "human":
                        user_messages += 1
                    elif msg.get("role") == "assistant":
                        ai_messages += 1
                    
                    # Group by date for trend chart
                    msg_date = msg.get("timestamp", chat.created_at)
                    if not isinstance(msg_date, datetime) and chat.created_at:
                        msg_date = chat.created_at
                        
                    if isinstance(msg_date, datetime):
                        date_key = msg_date.strftime("%Y-%m-%d")
                        message_dates[date_key] = message_dates.get(date_key, 0) + 1
    
    # Prepare chat trend data (last 7 days)
    chat_trend = []
    for i in range(7):
        date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
        chat_trend.append({
            "date": date,
            "count": message_dates.get(date, 0)
        })
    chat_trend.reverse()
    
    # Recent activity (last 5 chat sessions)
    recent_activity = []
    for chat in all_chats[:5]:
        try:
            # Get the last message from each chat
            last_message = None
            message_count = 0
            
            if hasattr(chat, 'messages') and chat.messages and len(chat.messages) > 0:
                message_count = len(chat.messages)
                last_message = chat.messages[-1] if message_count > 0 else None
            
            # Handle cases where chat_id or other fields might be missing
            chat_id = getattr(chat, 'chat_id', str(random.randint(1000, 9999)))
            title = getattr(chat, 'title', 'Untitled Chat')
            updated_at = getattr(chat, 'updated_at', datetime.utcnow())
            
            recent_activity.append({
                "id": chat_id,
                "time": updated_at,
                "title": title,
                "message_count": message_count,
                "last_message_type": last_message.get("role") if isinstance(last_message, dict) else None,
                "status": "completed" if message_count > 0 else "started"
            })
        except Exception as e:
            print(f"Error processing chat for recent activity: {e}")
    
    # Calculate stats
    avg_messages = total_messages / len(all_chats) if all_chats else 0
    
    # For demo purposes, we'll simulate these metrics
    # In a real app, you'd calculate these from actual user data
    completion_rate = (ai_messages / user_messages) * 100 if user_messages > 0 else 0
    
    return AnalyticsSummary(
        total_chats=len(all_chats),
        total_messages=total_messages,
        avg_messages_per_chat=round(avg_messages, 1),
        active_users=1,  # This would be calculated across all users in a real app
        completion_rate=round(completion_rate, 1),
        recent_activity=recent_activity,
        chat_trend=chat_trend,
        message_types={
            "user": user_messages,
            "assistant": ai_messages
        }
    )

@router.get("/chat-distribution")
async def get_chat_distribution(
    user_id: Annotated[str | None, Header()] = None
):
    """Get chat distribution data for charts"""
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id header")
    
    # Get all chat sessions for this user
    # Make sure to await the find operation
    chat_cursor = ChatSession.find({"user_id": user_id})
    chats = await chat_cursor.to_list()
    
    # Distribution by hour of day
    hour_distribution = {str(i): 0 for i in range(24)}
    day_distribution = {str(i): 0 for i in range(7)}  # 0=Monday, 6=Sunday
    
    for chat in chats:
        if chat.created_at:
            hour = chat.created_at.hour
            hour_distribution[str(hour)] += 1
            
            day = chat.created_at.weekday()
            day_distribution[str(day)] += 1
    
    return {
        "hour_distribution": [
            {"hour": hour, "count": count} 
            for hour, count in hour_distribution.items()
        ],
        "day_distribution": [
            {"day": day, "count": count} 
            for day, count in day_distribution.items()
        ]
    }
