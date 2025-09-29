from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import chat, control
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state variables for system control
ACCEPT_REQUESTS = True
ENERGY_MODE = settings.energy_mode

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Klein AI Dual Framework - Two AIs working together for safe, trustworthy AI interactions"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(control.router, prefix="/api", tags=["control"])

@app.get("/")
async def root():
    """Root endpoint with system info"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational" if ACCEPT_REQUESTS else "shutdown",
        "mode": ENERGY_MODE,
        "message": "Klein + Ophir: Two AIs. One helps. One protects."
    }

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Energy mode: {ENERGY_MODE}")
    logger.info(f"CORS origins: {settings.cors_origins}")

    # Log system startup
    from services.audit import audit_service
    audit_service.log_event("SYSTEM_STARTUP", {
        "version": settings.app_version,
        "energy_mode": ENERGY_MODE
    })

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("Shutting down Klein AI Dual Framework")

    # Log system shutdown
    from services.audit import audit_service
    audit_service.log_event("SYSTEM_SHUTDOWN", {
        "reason": "application_termination"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3001)
