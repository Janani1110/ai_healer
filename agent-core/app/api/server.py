from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.session import get_db, init_db
from app.api import routes

app = FastAPI(
    title="Self-Healing CI/CD Agent",
    description="AI-powered system for automatic CI/CD failure detection and repair",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    
    # Start the agent orchestrator
    from app.services.agent_orchestrator import AgentOrchestrator
    from loguru import logger
    
    logger.info("Starting AI-Powered Self-Healing CI/CD Agent")
    logger.info("Version: 1.0.0")
    
    orchestrator = AgentOrchestrator()
    
    # Start monitoring in background
    import asyncio
    asyncio.create_task(orchestrator.start_monitoring())
    
    logger.info("Agent monitoring started")

# Include routers
app.include_router(routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Self-Healing CI/CD Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
