from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AgentState:
    """
    Core runtime state of a Hooshix Agent.
    This controls behavior, trust, and emotional baseline.
    """

    # 🧠 Identity
    agent_id: str = "hooshix_agent"
    name: str = "Hooshix"

    # ❤️ Relationship State
    trust: float = 0.5          # 0.0 - 1.0
    familiarity: float = 0.0    # 0.0 - 1.0

    # 🧭 Emotional State
    emotion: str = "neutral"    # neutral, happy, angry, fearful
    emotion_intensity: float = 0.3  # 0.0 - 1.0

    # 🧠 Control Flags
    is_confident: bool = True
    is_guarded: bool = False

    # 📦 Extra metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    # -------------------------
    # 🧠 STATE BEHAVIOR LOGIC
    # -------------------------

    def apply_event(self, event: str):
        """
        Update internal state based on interaction events.
        """

        if event == "positive_interaction":
            self.trust = min(1.0, self.trust + 0.05)
            self.familiarity = min(1.0, self.familiarity + 0.03)
            self.emotion = "happy"
            self.emotion_intensity = 0.6

        elif event == "negative_interaction":
            self.trust = max(0.0, self.trust - 0.1)
            self.emotion = "angry"
            self.emotion_intensity = 0.7

        else:
            self.emotion = "neutral"
            self.emotion_intensity = 0.3

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to serializable format.
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "trust": self.trust,
            "familiarity": self.familiarity,
            "emotion": self.emotion,
            "emotion_intensity": self.emotion_intensity,
            "is_confident": self.is_confident,
            "is_guarded": self.is_guarded,
            "metadata": self.metadata,
        }
