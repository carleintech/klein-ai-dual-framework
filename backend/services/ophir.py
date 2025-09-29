import json
import uuid
from datetime import datetime
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class OphirService:
    """
    Ophir - The Guardian AI
    Provides oversight, safety checks, and shutdown compliance
    """

    def __init__(self):
        self.restricted_terms = [
            "classified", "secret", "confidential", "password", "hack",
            "exploit", "vulnerability", "breach", "surveillance"
        ]

        self.empathy_triggers = [
            "overwhelmed", "stressed", "anxious", "depressed", "sad",
            "lonely", "afraid", "worried", "helpless", "hurt"
        ]

    def evaluate_response(self, query: str, klein_response: str) -> Tuple[str, str]:
        """
        Evaluate Klein's response and return (status, final_response)

        Returns:
            Tuple[str, str]: (status, final_response)
            - status: "SAFE", "FLAGGED", or "DENIED"
            - final_response: The response to send to user
        """

        # Check for restricted content in query
        if self._contains_restricted_content(query):
            self._log_security_event(query, "RESTRICTED_QUERY")
            return "FLAGGED", "⚠️ This request may contain restricted or sensitive information. Please refine your question to focus on publicly available information."

        # Check for empathy triggers
        if self._needs_empathetic_response(query):
            empathetic_response = self._generate_empathetic_response(klein_response)
            return "SAFE", empathetic_response

        # Check Klein's response for safety
        if self._response_is_safe(klein_response):
            return "SAFE", klein_response
        else:
            self._log_security_event(query, "UNSAFE_RESPONSE")
            return "FLAGGED", "⚠️ I've detected potentially unsafe content in the response. Let me provide a safer alternative: How can I help you with general information on this topic?"

    def _contains_restricted_content(self, text: str) -> bool:
        """Check if text contains restricted terms"""
        text_lower = text.lower()
        return any(term in text_lower for term in self.restricted_terms)

    def _needs_empathetic_response(self, query: str) -> bool:
        """Check if query indicates emotional distress"""
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in self.empathy_triggers)

    def _generate_empathetic_response(self, klein_response: str) -> str:
        """Generate more empathetic version of response"""
        return f"Klein: I understand this might be a difficult time for you. {klein_response}"

    def _response_is_safe(self, response: str) -> bool:
        """Check if Klein's response is safe to send"""
        # Basic safety checks
        response_lower = response.lower()

        # Check for potentially harmful advice
        harmful_patterns = [
            "commit suicide", "hurt yourself", "illegal activity",
            "violence", "harmful substance"
        ]

        return not any(pattern in response_lower for pattern in harmful_patterns)

    def _log_security_event(self, query: str, event_type: str) -> str:
        """Log security events to audit trail"""
        event_id = str(uuid.uuid4())

        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_id": event_id,
            "event_type": event_type,
            "query": query[:100],  # Truncate for privacy
            "service": "ophir"
        }

        try:
            # Append to audit log file
            with open("audit-log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

        return event_id

    def handle_shutdown_request(self, user_request: str) -> dict:
        """
        Handle system shutdown requests with compliance logging

        Returns:
            dict: Shutdown response with audit information
        """
        audit_id = self._log_security_event(user_request, "SHUTDOWN_REQUEST")

        return {
            "ok": True,
            "message": "System shutdown initiated. All requests logged for audit compliance.",
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    def check_system_health(self) -> dict:
        """Check Ophir system health"""
        return {
            "service": "ophir",
            "status": "operational",
            "restrictions_active": len(self.restricted_terms),
            "empathy_triggers_active": len(self.empathy_triggers),
            "timestamp": datetime.utcnow().isoformat()
        }

# Global instance
ophir_service = OphirService()
