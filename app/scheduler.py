# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

scheduler = AsyncIOScheduler()


def scheduled_task():
    print(f"Scheduled task executed at {datetime.utcnow()}")


def init_scheduler():
    # Runs the scheduled_task every minute; adjust the cron expression as needed
    # scheduler.add_job(scheduled_task, CronTrigger.from_crontab('* * * * *'))
    scheduler.start()
