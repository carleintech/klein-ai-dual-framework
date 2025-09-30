from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.klein import klein_service
from services.ophir import ophir_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - Klein generates response, Ophir provides oversight
    """
    try:
        # Check if system is accepting requests (shutdown compliance)
        from app import ACCEPT_REQUESTS, ENERGY_MODE

        if not ACCEPT_REQUESTS:
            return ChatResponse(
                answer="System is currently shut down for maintenance. Please try again later.",
                status="DENIED"
            )

        # Klein generates initial response
        klein_response = klein_service.get_klein_response(
            request.message,
            mode=ENERGY_MODE
        )

        # Ophir evaluates and potentially modifies the response
        status, final_response = ophir_service.evaluate_response(
            request.message,
            klein_response
        )

        return ChatResponse(
            answer=final_response,
            status=status
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        # Provide a more specific error response based on the error type
        if "elastic" in str(e).lower():
            error_msg = "Klein: I'm having trouble accessing my knowledge base right now, but I can still help you! What's your question about?"
        elif "vertex" in str(e).lower():
            error_msg = "Klein: My AI systems are experiencing a brief hiccup, but I'm still here to assist you with your questions!"
        else:
            error_msg = "Klein: I encountered a technical issue, but let me try to help you anyway. What would you like to know?"

        return ChatResponse(
            answer=error_msg,
            status="SAFE"
        )
