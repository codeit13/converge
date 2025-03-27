from beanie import Document
from datetime import datetime
class RunHistory(Document):
    query: str
    response: str
    timestamp: datetime
    class Settings:
        name = "run_history"
