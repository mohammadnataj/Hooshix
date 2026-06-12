from hooshix.explain.trace import ExplainTrace
from hooshix.policy.policy_engine import PolicyEngine
from typing import Dict, Any
import logging

from hooshix.memory.memory_store import MemoryStore
from hooshix.core.agent_state import AgentState
from hooshix.llm.llm_client import LLMClient
from hooshix.explain.explain_engine import ExplainabilityEngine

logger = logging.getLogger(__name__)


class AgentRuntime:
    """
    Core brain of Hooshix Agent (controlled AI runtime)
    """

    def __init__(
        self,
        memory: MemoryStore,
        state: AgentState,
        llm: LLMClient,
        explain: ExplainabilityEngine = None
    ):
        """
        Initialize AgentRuntime
        """

        self.memory = memory
        self.state = state
        self.llm = llm
        self.explain = explain

        # 🧠 Control layers
        self.policy_engine = PolicyEngine()
        self.trace = ExplainTrace()

        logger.info("AgentRuntime initialized successfully")

    # -------------------------
    # 🧠 MAIN PIPELINE
    # -------------------------

    def process_input(self, user_id: str, message: str) -> Dict[str, Any]:
        try:
            self._validate_input(user_id, message)


# -------------------------
# POLICY CHECK
# -------------------------

policy_result = self.policy_engine.evaluate(
    message,
    self.state.to_dict()
)

decision = policy_result["decision"]

if decision == "block":
    return {
        "response": "Request blocked by policy engine.",
        "state": self.state.to_dict(),
        "memory_count": len(self.memory.memories),
        "reasoning": [
            f"Policy blocked request: {policy_result.get('reason')}"
        ]
    }

if decision == "modify":
    message = policy_result["input"]

    self.trace.add(
        f"Policy modified input ({policy_result.get('reason')})"
    )
            logger.info(f"Processing input from user: {user_id}")

            # 1. Store input
            self.memory.add_memory(
                content=f"User: {message}",
                metadata={"user_id": user_id}
            )

            # 2. State update
            self._update_state(message)

            # 3. Memory retrieval
            relevant_memory = self.memory.search_memory(message)

            # 4. Build prompt
            prompt = self._build_prompt(message, relevant_memory)

            # 5. Policy check
            policy_result = self.policy_engine.evaluate(message, self.state)

            if policy_result["decision"] == "block":
                self.trace.log({
                    "input": message,
                    "decision": "block",
                    "rule": policy_result.get("reason"),
                    "before": message,
                    "after": None
                })

                return self._error_response("Blocked by policy engine")

            if policy_result["decision"] == "modify":
                self.trace.log({
                    "input": message,
                    "decision": "modify",
                    "rule": policy_result.get("reason"),
                    "before": message,
                    "after": policy_result["input"]
                })
                message = policy_result["input"]

            else:
                self.trace.log({
                    "input": message,
                    "decision": "allow",
                    "rule": "none",
                    "before": message,
                    "after": message
                })

            # 6. LLM call
            response = self.llm.generate(prompt)

            # 7. Store response
            self.memory.add_memory(
                content=f"Agent: {response}",
                metadata={"type": "agent_response"}
            )

            # 8. Explainability engine (optional legacy)
            reasoning = []
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
                "memory_count": len(self.memory.memories),
                "trace": self.trace.get_all(),
                "reasoning": reasoning
            }

        except Exception as e:
            logger.error(f"Runtime error: {e}", exc_info=True)
            return self._error_response(str(e))

    # -------------------------
    # 🧠 VALIDATION
    # -------------------------

    def _validate_input(self, user_id: str, message: str):
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user_id")

        if not message or not isinstance(message, str):
            raise ValueError("Invalid message")

    # -------------------------
    # 🧠 STATE
    # -------------------------

    def _update_state(self, message: str):
        msg = message.lower()

        if any(w in msg for w in ["good", "great", "thanks"]):
            self.state.apply_event("positive_interaction")

        elif any(w in msg for w in ["bad", "angry", "hate"]):
            self.state.apply_event("negative_interaction")

        else:
            self.state.apply_event("neutral_chat")

    # -------------------------
    # 🧠 ERROR HANDLER
    # -------------------------

    def _error_response(self, error: str):
        return {
            "response": f"Error: {error}",
            "state": self.state.to_dict(),
            "memory_count": len(self.memory.memories),
            "trace": self.trace.get_all(),
            "error": error
        }

    # -------------------------
    # 🧠 PROMPT BUILDER (simple fallback)
    # -------------------------

    def _build_prompt(self, message, memory):
        mem_text = "\n".join([m["content"] for m in memory]) if memory else ""
        return f"Memory:\n{mem_text}\n\nUser: {message}\nAssistant:"
