# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from uuid import uuid4
from models.run_history import Message, ChatSession
from services.agent_service import AgentService
from datetime import datetime

scheduler = AsyncIOScheduler()


async def scheduled_task():
    task = "Search for latest articles on tech in AI related to coding, and write an article"
    agent_service: AgentService = AgentService()
    try:
        result = await agent_service.run(task)
    except Exception as e:
        raise Exception(status_code=500, detail=str(e))

    # Create messages for the chat session
    messages = [
        Message(
            message_id=str(uuid4()),
            role="system",
            content=task,
            timestamp=datetime.utcnow(),
            metadata={"type": "scheduled_task"}
        )
    ]

    if result.get("messages"):
        response_content = result["messages"][-1].content
        messages.append(
            Message(
                message_id=str(uuid4()),
                role="assistant",
                content=response_content,
                timestamp=datetime.utcnow(),
                metadata={"type": "scheduled_response"}
            )
        )

    # Create a chat session for this scheduled task
    chat_session = ChatSession(
        chat_id=str(uuid4()),
        title="Scheduled Task: AI Tech Article",
        messages=messages,
        agent_name=agent_service.agent_name,
        user_id="system",  # Use system as the user for scheduled tasks
        metadata={"task_type": "scheduled_article_generation"}
    )
    await chat_session.insert()
    print(f"Scheduled task executed and saved at {datetime.utcnow()}")


def init_scheduler():
    # Runs the scheduled_task every minute; adjust the cron expression as needed
    # scheduler.add_job(scheduled_task, CronTrigger.from_crontab('* * * * *'))
    # scheduler.start()
    pass
