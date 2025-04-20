from signal import signal, SIGINT, SIGTERM
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from api.endpoints import agent_router, analytics_router, rag_router
from services.agent_service import AgentService
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.run_history import Message, ChatSession
from scheduler import init_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent_service = AgentService()

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.MONGODB_DB], document_models=[Message, ChatSession])

    print("FastAPI app initialized")

    try:
        await app.state.agent_service.initialize()
        init_scheduler()
        yield
    except Exception as e:
        print(f"Error during app startup: {e}")
    finally:
        print("Shutting down services...")
        await app.state.agent_service.shutdown()
        print("Shutdown complete")

app = FastAPI(title="Converge API", version="1.0.0", lifespan=lifespan)

# CORS must not use '*' when allow_credentials=True; use the specific frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai.sleebit.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")
app.include_router(analytics_router, prefix="/api/analytics")
app.include_router(rag_router, prefix="/api/rag")


@app.get("/health")
def health():
    return {"status": "ok"}


def handle_shutdown_signal(signal, frame):
    print("Shutdown signal received. Cleaning up...")
    # Perform cleanup actions here
    sys.exit(0)


signal(SIGINT, handle_shutdown_signal)
signal(SIGTERM, handle_shutdown_signal)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
