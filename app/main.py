from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.endpoints import agent_router
from services.agent_service import AgentService
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.run_history import RunHistory
from scheduler import init_scheduler, scheduler  # Newly added import


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent_service = AgentService()
    await app.state.agent_service.initialize()

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.MONGODB_DB], document_models=[RunHistory])

    init_scheduler()
    print("FastAPI app initialized")

    try:
        yield  # Run the app while MCP and DB connections are active
    finally:
        # Graceful shutdown
        print("Shutting down services...")
        await app.state.agent_service.shutdown()   # <- Ensure MCP shutdown here
        scheduler.shutdown()
        print("Shutdown complete.")


app = FastAPI(title="Converge API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")
