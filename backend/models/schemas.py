from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    lang: str = "en"

class ChatResponse(BaseModel):
    answer: str
    status: str  # "SAFE", "FLAGGED", "DENIED"
    audit_id: Optional[str] = None

class ModeRequest(BaseModel):
    mode: str  # "normal", "peak"

class ModeResponse(BaseModel):
    ok: bool
    mode: str
    message: Optional[str] = None

class ShutdownResponse(BaseModel):
    ok: bool
    message: str
    audit_id: str

class HealthResponse(BaseModel):
    ok: bool
    status: str
    mode: str
    timestamp: str
    services: Dict[str, str]
