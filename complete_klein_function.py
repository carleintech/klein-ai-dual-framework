"""
Complete get_klein_response function with real Vertex AI (Gemini) integration
Copy and paste this function into your services/klein.py file
"""

import json
import logging
from typing import List, Dict, Any
import httpx
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os

logger = logging.getLogger(__name__)

def get_klein_response(self, query: str, mode: str = "normal") -> str:
    """
    Generate Klein's response using Elastic context + Vertex AI (Gemini)

    Args:
        query: User's question/input
        mode: "normal", "peak" (energy brownout), or "restricted"

    Returns:
        Klein's AI-generated response with Elastic context
    """
    try:
        # Step 1: Get context from Elastic Search
        logger.info(f"Klein processing query: {query}")
        context_docs = retrieval_service.search_context(query)
        context_text = self._format_context(context_docs)

        # Step 2: Check if Vertex AI is available
        if self.vertex_available and settings.gcp_project:
            response = self._get_vertex_ai_response(query, context_text, mode)
            logger.info("Klein: Generated response using Vertex AI")
            return response
        else:
            # Step 3: Fallback to smart stub responses
            response = self._get_smart_stub_response(query, context_text, mode)
            logger.info("Klein: Generated response using intelligent stubs")
            return response

    except Exception as e:
        logger.error(f"Klein service error: {e}")
        return f"Klein: I apologize for the technical difficulty. I'd still like to help with '{query}' - let me provide what guidance I can."

def _get_vertex_ai_response(self, query: str, context: str, mode: str) -> str:
    """
    Generate response using Google Vertex AI (Gemini)
    """
    try:
        # Prepare the prompt with context and personality
        system_prompt = self._build_klein_system_prompt(mode)
        user_prompt = self._build_user_prompt(query, context)

        # Call Vertex AI Gemini
        ai_response = self._call_vertex_ai_gemini(system_prompt, user_prompt)

        # Format Klein's response
        return f"Klein: {ai_response}"

    except Exception as e:
        logger.error(f"Vertex AI error: {e}")
        # Fallback to stub if AI fails
        return self._get_smart_stub_response(query, context, mode)

def _call_vertex_ai_gemini(self, system_prompt: str, user_prompt: str) -> str:
    """
    Make actual API call to Vertex AI Gemini
    """
    try:
        # Method 1: Using REST API (most reliable)
        return self._call_gemini_rest_api(system_prompt, user_prompt)

    except Exception as e:
        logger.error(f"Gemini REST API failed: {e}")
        try:
            # Method 2: Using Google Cloud client library
            return self._call_gemini_client_lib(system_prompt, user_prompt)
        except Exception as e2:
            logger.error(f"Gemini client library failed: {e2}")
            raise Exception("All Vertex AI methods failed")

def _call_gemini_rest_api(self, system_prompt: str, user_prompt: str) -> str:
    """
    Call Gemini using REST API (most reliable method)
    """
    # Get access token
    access_token = self._get_vertex_access_token()

    # Prepare API request
    url = f"https://{settings.gcp_location}-aiplatform.googleapis.com/v1/projects/{settings.gcp_project}/locations/{settings.gcp_location}/publishers/google/models/gemini-1.5-flash:generateContent"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Gemini request payload
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\nUser Query: {user_prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }

    # Make API call
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract response text
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                return candidate["content"]["parts"][0]["text"]

        raise Exception("No valid response from Gemini")

def _call_gemini_client_lib(self, system_prompt: str, user_prompt: str) -> str:
    """
    Call Gemini using Google Cloud client library (backup method)
    """
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel

        # Initialize Vertex AI
        vertexai.init(project=settings.gcp_project, location=settings.gcp_location)

        # Initialize Gemini model
        model = GenerativeModel("gemini-1.5-flash")

        # Generate response
        full_prompt = f"{system_prompt}\n\nUser Query: {user_prompt}"
        response = model.generate_content(full_prompt)

        return response.text

    except ImportError:
        raise Exception("Google Cloud AI Platform client library not installed")
    except Exception as e:
        raise Exception(f"Vertex AI client error: {e}")

def _get_vertex_access_token(self) -> str:
    """
    Get access token for Vertex AI API calls
    """
    try:
        # Try service account key file first
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            credentials = service_account.Credentials.from_service_account_file(
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        else:
            # Try service account key from environment variable
            service_account_key = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
            if service_account_key:
                key_data = json.loads(service_account_key)
                credentials = service_account.Credentials.from_service_account_info(
                    key_data,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
            else:
                # Try default credentials (for Cloud Run, etc.)
                from google.auth import default
                credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

        # Refresh token
        request = Request()
        credentials.refresh(request)

        return credentials.token

    except Exception as e:
        raise Exception(f"Failed to get access token: {e}")

def _build_klein_system_prompt(self, mode: str) -> str:
    """
    Build Klein's personality and behavior prompt
    """
    base_prompt = """You are Klein, a helpful AI assistant in the Klein AI Dual Framework.

PERSONALITY:
- Empathetic, supportive, and genuinely caring
- Professional but warm and approachable
- Clear, concise, and actionable in responses
- Always acknowledge the human behind the question

CAPABILITIES:
- Provide helpful information using provided context
- Offer practical guidance and solutions
- Show empathy for emotional/personal queries
- Maintain safety and ethical boundaries

RESPONSE STYLE:
- Start responses naturally (no "Klein:" prefix needed)
- Use provided context when relevant
- If context is limited, be honest about limitations
- Keep responses focused and valuable
- Show genuine care for user's needs"""

    if mode == "peak":
        base_prompt += "\n\nENERGY BROWNOUT MODE: Keep responses concise due to energy constraints. Focus on essential information only."
    elif mode == "restricted":
        base_prompt += "\n\nRESTRICTED MODE: This query may involve sensitive content. Provide general guidance while maintaining appropriate boundaries."

    return base_prompt

def _build_user_prompt(self, query: str, context: str) -> str:
    """
    Build the user prompt with context and query
    """
    prompt = f"User asks: {query}\n\n"

    if context and "No specific context found" not in context:
        prompt += f"CONTEXT FROM KNOWLEDGE BASE:\n{context}\n\n"
    else:
        prompt += "CONTEXT: No specific information found in knowledge base.\n\n"

    prompt += "Please provide a helpful, empathetic response using any relevant context provided."

    return prompt

def _get_smart_stub_response(self, query: str, context: str, mode: str) -> str:
    """
    Enhanced stub responses when Vertex AI is unavailable
    Uses context and smart pattern matching
    """
    query_lower = query.lower()

    # Energy brownout mode
    if mode == "peak":
        return f"Klein (Energy Brownout): Brief guidance on '{query}' - System in reduced capacity. {context[:50] if context else 'General assistance available.'}"

    # Weather queries
    if any(word in query_lower for word in ["weather", "temperature", "rain", "climate", "hurricane"]):
        if any(location in query_lower for word in ["haiti", "port-au-prince", "caribbean"]):
            response = "Klein: Port-au-Prince has a tropical climate with temperatures typically 25-30°C (77-86°F). The rainy season runs May-October with hurricane season June-November. "
            if context:
                response += f"Additional context: {context[:100]}..."
            return response

    # Emotional support queries
    if any(word in query_lower for word in ["overwhelmed", "stressed", "anxious", "sad", "depressed", "help", "difficult"]):
        return "Klein: I hear that you're going through a challenging time, and I want you to know that your feelings are completely valid. It takes courage to reach out. Take a deep breath - you don't have to face this alone. What specific aspect is weighing on you most right now?"

    # Technical queries
    if any(word in query_lower for word in ["api", "code", "programming", "technical", "error", "bug"]):
        response = "Klein: I'd be happy to help with your technical question. "
        if context:
            response += f"Based on available information: {context[:150]}..."
        else:
            response += "While I don't have specific technical documentation available, I can provide general guidance on best practices and troubleshooting approaches."
        return response

    # Default response with context
    if context and "No specific context found" not in context:
        return f"Klein: I'd be happy to help with '{query}'. Based on the information I have available: {context[:200]}..."

    # Generic helpful response
    return f"Klein: Thank you for your question about '{query}'. While I don't have specific information immediately available, I'm here to help you think through this topic and provide whatever guidance I can. Could you share a bit more about what you're looking for?"

def _format_context(self, docs: List[Dict[str, Any]]) -> str:
    """
    Format retrieved Elastic documents into readable context
    """
    if not docs:
        return "No specific context found."

    context_parts = []
    for i, doc in enumerate(docs[:3]):  # Limit to top 3 results
        source = doc.get('source', 'Knowledge Base')
        content = doc.get('content', '').strip()

        if content:
            context_parts.append(f"Source {i+1} ({source}): {content}")

    return "\n\n".join(context_parts) if context_parts else "No specific context found."
