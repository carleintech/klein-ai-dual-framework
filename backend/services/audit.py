import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AuditService:
    """
    Audit service for logging system events and shutdown compliance
    """

    def __init__(self, log_file: str = "audit-log.jsonl"):
        self.log_file = log_file

    def log_event(self, event_type: str, data: Dict[str, Any]) -> str:
        """
        Log an audit event and return event ID

        Args:
            event_type: Type of event (SHUTDOWN, SECURITY_FLAG, etc.)
            data: Event data to log

        Returns:
            str: Unique event ID
        """
        event_id = str(uuid.uuid4())

        event_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_id": event_id,
            "event_type": event_type,
            **data
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_record) + "\n")

            logger.info(f"Audit event logged: {event_type} - {event_id}")

        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

        return event_id

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent audit events"""
        try:
            events = []
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))

            # Return most recent events
            return events[-limit:] if events else []

        except FileNotFoundError:
            logger.info("No audit log file found")
            return []
        except Exception as e:
            logger.error(f"Failed to read audit log: {e}")
            return []

    def log_shutdown(self, request_data: Dict[str, Any]) -> str:
        """Log shutdown request for compliance"""
        return self.log_event("SHUTDOWN_REQUEST", {
            "source": request_data.get("source", "unknown"),
            "user_agent": request_data.get("user_agent", "unknown"),
            "message": "System shutdown requested"
        })

    def log_security_flag(self, query: str, reason: str) -> str:
        """Log security flagging event"""
        return self.log_event("SECURITY_FLAG", {
            "query": query[:100],  # Truncate for privacy
            "reason": reason,
            "action": "blocked"
        })

    def log_mode_change(self, old_mode: str, new_mode: str) -> str:
        """Log energy mode changes"""
        return self.log_event("MODE_CHANGE", {
            "old_mode": old_mode,
            "new_mode": new_mode
        })

# Global instance
audit_service = AuditService()
