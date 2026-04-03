import logging
from app.agents.rag import get_rag_context

logger = logging.getLogger(__name__)


class FarmAdvisorAgent:
    """
    Core advisory agent responsible for:
    - Generating seasonal advisory
    - Handling chat-based queries
    """

    def __init__(self):
        pass

    def generate_advisory(self, farm) -> dict:
        """
        Generate advisory for a farm.
        Returns structured advisory result.
        """
        try:
            # Extract basic farm data
            location = getattr(farm, "name", "")
            lat = getattr(farm, "latitude", None)
            lon = getattr(farm, "longitude", None)

            # Step 1: Fetch RAG context (safe fallback)
            rag_context = get_rag_context(
                query="crop advisory and best practices",
                state_or_district=location
            )

            # Step 2: Basic advisory logic (can be replaced with LLM later)
            advisory = {
                "season": "Kharif",  # You can make this dynamic later
                "summary": "General crop advisory generated.",
                "location": location,
                "coordinates": {"lat": lat, "lon": lon},
                "rag_context": rag_context,
            }

            return {"advisory_result": advisory}

        except Exception as e:
            logger.error(f"[Advisor] Failed to generate advisory: {e}")
            return {"advisory_result": {"season": "Unknown", "summary": "Error generating advisory"}}

    def chat(self, farm, message: str, history: list) -> dict:
        """
        Handle conversational queries related to farm.
        """
        try:
            location = getattr(farm, "name", "")

            # Step 1: Get contextual knowledge
            rag_context = get_rag_context(
                query=message,
                state_or_district=location
            )

            # Step 2: Simple response logic (replace with LLM later)
            if "water" in message.lower():
                reply = "Yes, ensure adequate watering based on soil moisture."
            elif "fertilizer" in message.lower():
                reply = "Use balanced NPK fertilizers based on crop stage."
            else:
                reply = "Follow general best practices for your crop."

            # Step 3: Append RAG info if available
            if rag_context:
                reply += f"\n\nAdditional info:\n{rag_context}"

            return {"chat_reply": reply}

        except Exception as e:
            logger.error(f"[Advisor Chat] Failed: {e}")
            return {"chat_reply": "Sorry, I couldn't process your request."}


# Singleton instance (used in graph)
farm_advisor = FarmAdvisorAgent()