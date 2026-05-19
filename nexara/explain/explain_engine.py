from typing import Dict, Any, List
import time


class ExplainabilityEngine:
    """
    Tracks why an agent made a decision.
    Provides transparency for debugging and control.
    """

    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    # -------------------------
    # 🧠 LOG DECISION
    # -------------------------

    def log_decision(
        self,
        user_input: str,
        prompt: str,
        memory_used: List[Dict],
        state_snapshot: Dict,
        response: str
    ):
        log_entry = {
            "timestamp": time.time(),
            "user_input": user_input,
            "prompt": prompt,
            "memory_used": memory_used,
            "state_snapshot": state_snapshot,
            "response": response,
            "reasoning": self._generate_reason(state_snapshot, memory_used)
        }

        self.logs.append(log_entry)
        return log_entry

    # -------------------------
    # 🧠 SIMPLE REASONING (Phase 1)
    # -------------------------

    def _generate_reason(self, state: Dict, memory: List[Dict]) -> List[str]:
        reasons = []

        if state.get("trust", 0) < 0.4:
            reasons.append("Low trust influenced cautious response")

        if state.get("emotion") == "happy":
            reasons.append("Positive emotional state detected")

        if len(memory) > 0:
            reasons.append("Relevant past memory was used")

        if state.get("is_guarded"):
            reasons.append("Agent is in guarded mode")

        if not reasons:
            reasons.append("Default controlled response behavior")

        return reasons

    # -------------------------
    # 🧠 RETRIEVE LOGS
    # -------------------------

    def get_logs(self):
        return self.logs

    def clear_logs(self):
        self.logs = []
