from core.config import settings
from services.retrieval import retrieval_service
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class KleinService:
    def __init__(self):
        self.vertex_available = bool(settings.gcp_project)

    def get_klein_response(self, query: str, mode: str = "normal") -> str:
        """
        Generate Klein's response using retrieval + Vertex AI
        Falls back to deterministic responses if services unavailable
        """
        try:
            # Get context from retrieval service
            context_docs = retrieval_service.search_context(query)
            context_text = self._format_context(context_docs)

            if self.vertex_available:
                return self._vertex_ai_response(query, context_text, mode)
            else:
                return self._stub_response(query, context_text, mode)

        except Exception as e:
            logger.error(f"Klein service error: {e}")
            return f"Klein: I apologize, but I'm experiencing technical difficulties. However, I can help you with general information about: {query}"

    def _format_context(self, docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context"""
        if not docs:
            return "No specific context found."

        context_parts = []
        for doc in docs:
            context_parts.append(f"Source: {doc.get('source', 'Unknown')}\n{doc.get('content', '')}")

        return "\n\n".join(context_parts)

    def _vertex_ai_response(self, query: str, context: str, mode: str) -> str:
        """Generate response using Vertex AI (to be implemented)"""
        # TODO: Implement actual Vertex AI integration
        # For now, return a structured response

        if mode == "peak":
            return f"Klein (Brownout Mode): {query} - Brief response due to energy constraints. Context: {context[:100]}..."

        return f"Klein (Vertex AI): Based on available information, here's my response to '{query}'. Context considered: {context[:200]}..."

    def _stub_response(self, query: str, context: str, mode: str) -> str:
        """Fallback response when Vertex AI is not available"""

        # Handle common query patterns
        query_lower = query.lower()

        if any(word in query_lower for word in ["weather", "temperature", "rain", "climate"]):
            if "port-au-prince" in query_lower or "haiti" in query_lower:
                return "Klein: Port-au-Prince typically experiences tropical weather with temperatures around 25-30°C. During hurricane season (June-November), expect afternoon thunderstorms. Please monitor local weather services for current conditions."

        if any(word in query_lower for word in ["overwhelmed", "stressed", "anxious", "help"]):
            return "Klein: I understand you're going through a difficult time. It's completely normal to feel overwhelmed sometimes. Take a moment to breathe, and remember that you don't have to face this alone. Would you like to talk about what's causing these feelings?"

        if mode == "peak":
            return f"Klein (Energy Brownout): Short response to '{query}' - System operating in reduced capacity mode."

        # Default response with context if available
        if context and "No specific context found" not in context:
            return f"Klein: Based on available information about '{query}', I can provide some guidance. {context[:150]}..."

        return f"Klein: I'd be happy to help you with '{query}'. While I don't have specific information immediately available, I can provide general assistance and guidance on this topic."

# Global instance
klein_service = KleinService()
