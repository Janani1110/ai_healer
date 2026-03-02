import asyncio
import uvicorn
from loguru import logger
from app.core.config import settings
from app.api.server import app

if __name__ == "__main__":
    # Start the FastAPI server with the agent
    uvicorn.run(
        "app.api.server:app",
        host="0.0.0.0",
        port=settings.AGENT_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
