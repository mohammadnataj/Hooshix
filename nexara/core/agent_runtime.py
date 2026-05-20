from typing import Dict, Any

from nexara.memory.memory_store import MemoryStore
from nexara.core.agent_state import AgentState
from nexara.llm.llm_client import LLMClient
from nexara.explain.explain_engine import ExplainabilityEngine


class AgentRuntime:
    """
    Core brain of Nexara Agent (LLM-connected version)
    """

    def __init__(self, memory: MemoryStore, state: AgentState, llm: LLMClient, explain: ExplainabilityEngine = None):
        self.memory = memory
        self.state = state
        self.llm = llm
        self.explain = explain

    # -------------------------
    # 🧠 MAIN PIPELINE
    # -------------------------

    def process_input(self, user_id: str, message: str) -> Dict[str, Any]:

        # 1. Store user message
        self.memory.add_memory(
            content=f"User: {message}",
            metadata={"user_id": user_id}
        )

        # 2. Update agent state
        self._update_state(message)

        # 3. Retrieve relevant memory
        relevant_memory = self.memory.search_memory(message)

        # 4. Build prompt
        prompt = self._build_prompt(message, relevant_memory)

        # 5. Call LLM (REAL INTELLIGENCE)
        response = self.llm.generate(prompt)

        # 6. Store agent response
        self.memory.add_memory(
            content=f"Agent: {response}",
            metadata={"type": "agent_response"}
        )

        # 7. Log decision for explainability
        if self.explain:
            self.explain.log_decision(
                user_input=message,
                prompt=prompt,
                memory_used=relevant_memory,
                state_snapshot=self.state.to_dict(),
                response=response
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

        msg = message.lower()

        if any(w in msg for w in ["thanks", "good", "great", "nice"]):
            self.state.apply_event("positive_interaction")

        elif any(w in msg for w in ["bad", "hate", "angry", "stupid"]):
            self.state.apply_event("negative_interaction")

        else:
            self.state.apply_event("neutral_chat")

    # -------------------------
    # 🧠 PROMPT ENGINE
    # -------------------------

    def _build_prompt(self, message: str, memory: list) -> str:

        memory_text = "\n".join(
            [m["content"] for m in memory[-5:]]
        )

        prompt = f"""
You are Nexara, a controlled AI Agent.

You have:
- Persistent memory
- Emotional state
- Trust system
- Behavioral rules

Current State:
- Name: {self.state.name}
- Emotion: {self.state.emotion} ({self.state.emotion_intensity})
- Trust: {self.state.trust}
- Familiarity: {self.state.familiarity}

Recent Memory:
{memory_text}

User Message:
{message}

Rules:
- Be consistent with your personality
- Do not break character
- Use memory when relevant
- Respond naturally but controlled

Now respond:
"""

        return prompt
