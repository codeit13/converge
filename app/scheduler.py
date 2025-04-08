# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from models.run_history import RunHistory
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

    response_content = ""
    if result.get("messages"):
        response_content = result["messages"][-1].content
    run_doc = RunHistory(query=task,
                         response=response_content, timestamp=datetime.utcnow())
    await run_doc.insert()
    print(f"Scheduled task executed at {datetime.utcnow()}")


def init_scheduler():
    # Runs the scheduled_task every minute; adjust the cron expression as needed
    # scheduler.add_job(scheduled_task, CronTrigger.from_crontab('* * * * *'))
    # scheduler.start()
    pass
