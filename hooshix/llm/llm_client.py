import os
from typing import Optional


class LLMClient:
    """
    Abstraction layer for LLM providers.
    Hooshix does NOT depend on a single model.
    """

    def __init__(self, provider: str = "mock"):
        self.provider = provider

        # future: API keys
        self.api_key = os.getenv("LLM_API_KEY", None)

    # -------------------------
    # 🧠 MAIN CALL
    # -------------------------

    def generate(self, prompt: str) -> str:
        """
        Main interface for generating responses
        """

        if self.provider == "mock":
            return self._mock_response(prompt)

        elif self.provider == "openai":
            return self._openai_response(prompt)

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    # -------------------------
    # 🧪 MOCK (Phase 1 fallback)
    # -------------------------

    def _mock_response(self, prompt: str) -> str:
        """
        Deterministic fallback for testing system flow
        """

        if "trust" in prompt.lower():
            return "Trust level is being evaluated."

        if "emotion" in prompt.lower():
            return "Emotion state acknowledged."

        return "I am Hooshix Agent responding in controlled mode."

    # -------------------------
    # 🤖 OPENAI INTEGRATION (Phase 2)
    # -------------------------

    def _openai_response(self, prompt: str) -> str:
        """
        Real LLM call (placeholder structure)
        """

        # NOTE: actual SDK integration will be added later
        # keeping structure clean for now

        if not self.api_key:
            return "Missing API key for LLM provider."

        # pseudo-response (we will replace with real API call)
        return f"[OPENAI RESPONSE MOCKED]\n{prompt[:200]}"
