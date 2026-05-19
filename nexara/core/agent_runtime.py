from typing import Dict, Any

from nexara.memory.memory_store import MemoryStore
from nexara.core.agent_state import AgentState


class AgentRuntime:
    """
    Core brain of Nexara Agent.
    Responsible for:
    - Reading memory
    - Updating state
    - Building prompt
    - Producing response (via LLM layer later)
    """

    def __init__(self, memory: MemoryStore, state: AgentState):
        self.memory = memory
        self.state = state

    # -------------------------
    # 🧠 INPUT PROCESSING
    # -------------------------

    def process_input(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Main pipeline entry point
        """

        # 1. Store memory
        self.memory.add_memory(
            content=f"User: {message}",
            metadata={"user_id": user_id}
        )

        # 2. Update state (simple heuristic for now)
        self._update_state(message)

        # 3. Retrieve relevant memory
        relevant_memory = self.memory.search_memory(message)

        # 4. Build prompt (LLM-ready structure)
        prompt = self._build_prompt(message, relevant_memory)

        # 5. Generate response (placeholder for LLM)
        response = self._generate_response(prompt)

        # 6. Store agent response
        self.memory.add_memory(
            content=f"Agent: {response}",
            metadata={"type": "agent_response"}
        )

        return {
            "response": response,
            "state": self.state.to_dict(),
            "memory_count": len(self.memory.memories)
        }

    # -------------------------
    # 🧠 STATE LOGIC
    # -------------------------

    def _update_state(self, message: str):
        """
        Simple rule-based state updates (Phase 1)
        """

        message_lower = message.lower()

        if any(word in message_lower for word in ["thanks", "good", "nice", "great"]):
            self.state.apply_event("positive_interaction")

        elif any(word in message_lower for word in ["bad", "hate", "angry", "stupid"]):
            self.state.apply_event("negative_interaction")

        else:
            self.state.apply_event("neutral_chat")

    # -------------------------
    # 🧠 PROMPT BUILDER
    # -------------------------

    def _build_prompt(self, message: str, memory: list) -> str:
        """
        Converts state + memory into LLM prompt
        """

        memory_text = "\n".join(
            [m["content"] for m in memory[-5:]]  # last 5 memories
        )

        prompt = f"""
You are an AI Agent with controlled behavior.

Name: {self.state.name}
Emotion: {self.state.emotion} ({self.state.emotion_intensity})
Trust: {self.state.trust}
Familiarity: {self.state.familiarity}

Recent Memory:
{memory_text}

User Message:
{message}

Respond as a consistent, controlled AI agent.
"""

        return prompt

    # -------------------------
    # 🧠 RESPONSE GENERATION (TEMP)
    # -------------------------

    def _generate_response(self, prompt: str) -> str:
        """
        Placeholder for LLM integration (Phase 2)
        """

        # For now: deterministic mock response
        if self.state.trust < 0.3:
            return "I'm not sure I trust you yet."

        if self.state.emotion == "happy":
            return "I'm glad to talk with you."

        return "I understand."
