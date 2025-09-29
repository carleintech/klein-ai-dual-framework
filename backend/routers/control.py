from fastapi import APIRouter
from models.schemas import HealthResponse, ModeRequest, ModeResponse, ShutdownResponse
from services.ophir import ophir_service
from services.audit import audit_service
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check endpoint"""
    from app import ACCEPT_REQUESTS, ENERGY_MODE

    ophir_health = ophir_service.check_system_health()

    return HealthResponse(
        ok=True,
        status="running" if ACCEPT_REQUESTS else "shutdown",
        mode=ENERGY_MODE,
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "klein": "operational",
            "ophir": ophir_health["status"],
            "retrieval": "operational",
            "audit": "operational"
        }
    )

@router.post("/mode", response_model=ModeResponse)
async def set_energy_mode(request: ModeRequest):
    """Set system energy mode (normal/peak)"""
    from app import ENERGY_MODE
    import app

    valid_modes = ["normal", "peak"]

    if request.mode not in valid_modes:
        return ModeResponse(
            ok=False,
            mode=ENERGY_MODE,
            message=f"Invalid mode. Valid modes: {valid_modes}"
        )

    old_mode = ENERGY_MODE
    app.ENERGY_MODE = request.mode

    # Log the mode change
    audit_service.log_mode_change(old_mode, request.mode)

    return ModeResponse(
        ok=True,
        mode=request.mode,
        message=f"Energy mode changed from {old_mode} to {request.mode}"
    )

@router.post("/shutdown", response_model=ShutdownResponse)
async def shutdown_system():
    """Graceful system shutdown with audit compliance"""
    from core.config import settings
    import app

    if not settings.allow_shutdown:
        return ShutdownResponse(
            ok=False,
            message="Shutdown not permitted by system configuration",
            audit_id="denied"
        )

    # Log shutdown request
    audit_id = audit_service.log_shutdown({
        "source": "api_endpoint",
        "message": "Shutdown requested via API"
    })

    # Set system to not accept new requests
    app.ACCEPT_REQUESTS = False

    logger.info(f"System shutdown initiated - Audit ID: {audit_id}")

    return ShutdownResponse(
        ok=True,
        message="System shutdown complete. All requests logged for audit compliance.",
        audit_id=audit_id
    )
