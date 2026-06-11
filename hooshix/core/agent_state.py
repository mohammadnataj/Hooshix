from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AgentState:
    """
    Core runtime state of a Hooshix Agent.
    This controls behavior, trust, and emotional baseline.
    """

    # 🧠 Identity
    agent_id: str = "nexara_agent"
    name: str = "Hooshix"

    # ❤️ Relationship State
    trust: float = 0.5          # 0.0 - 1.0
    familiarity: float = 0.0    # 0.0 - 1.0

    # 🧭 Emotional State (simple controlled model)
    emotion: str = "neutral"    # neutral, happy, angry, fearful, curious
    emotion_intensity: float = 0.3  # 0.0 - 1.0

    # 🧠 Context flags
    is_confident: bool = True
    is_guarded: bool = False

    # 📦 Extra extensibility layer
    metadata: Dict[str, Any] = field(default_factory=dict)

    # -------------------------
    # 🧠 STATE UPDATE METHODS
    # -------------------------

    def update_trust(self, delta: float):
        self.trust = max(0.0, min(1.0, self.trust + delta))

    def update_familiarity(self, delta: float):
        self.familiarity = max(0.0, min(1.0, self.familiarity + delta))

    def set_emotion(self, emotion: str, intensity: float = 0.5):
        self.emotion = emotion
        self.emotion_intensity = max(0.0, min(1.0, intensity))

    def apply_event(self, event: str):
        """
        Simple rule-based state transitions (Phase 1 logic)
        """
        if event == "positive_interaction":
            self.update_trust(0.05)
            self.update_familiarity(0.03)
            self.set_emotion("happy", 0.4)

        elif event == "negative_interaction":
            self.update_trust(-0.07)
            self.set_emotion("fearful", 0.6)
            self.is_guarded = True

        elif event == "neutral_chat":
            self.update_familiarity(0.01)
            self.set_emotion("neutral", 0.2)

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "trust": self.trust,
            "familiarity": self.familiarity,
            "emotion": self.emotion,
            "emotion_intensity": self.emotion_intensity,
            "is_confident": self.is_confident,
            "is_guarded": self.is_guarded,
            "metadata": self.metadata
        }
