from dataclasses import dataclass
from typing import Any, Dict, List, Callable


class PolicyDecision:
    ALLOW = "allow"
    MODIFY = "modify"
    BLOCK = "block"


@dataclass
class PolicyResult:
    decision: str
    input: str
    reason: str = ""
    score: float = 1.0


class PolicyRule:
    def __init__(self, name: str, condition: Callable, action: Callable = None, priority: int = 1):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority

    def matches(self, text: str, state: Dict[str, Any]) -> bool:
        return self.condition(text, state)

    def apply(self, text: str, state: Dict[str, Any]):
        if self.action:
            return self.action(text, state)
        return text


class PolicyEngine:
    """
    Advanced Governance Engine for Hooshix
    """

    def __init__(self, rules: List[PolicyRule] = None):
        self.rules = rules or []

    def add_rule(self, rule: PolicyRule):
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def evaluate(self, input_text: str, state: Dict[str, Any] = None) -> Dict[str, Any]:

        state = state or {}

        for rule in self.rules:

            if rule.matches(input_text, state):

                result = rule.apply(input_text, state)

                # BLOCK RULE
                if isinstance(result, dict) and result.get("decision") == PolicyDecision.BLOCK:
                    return {
                        "decision": PolicyDecision.BLOCK,
                        "input": input_text,
                        "reason": rule.name,
                        "score": 0.0
                    }

                # MODIFY RULE
                if isinstance(result, dict) and result.get("decision") == PolicyDecision.MODIFY:
                    return {
                        "decision": PolicyDecision.MODIFY,
                        "input": result.get("input", input_text),
                        "reason": rule.name,
                        "score": 0.7
                    }

        # DEFAULT
        return {
            "decision": PolicyDecision.ALLOW,
            "input": input_text,
            "reason": "default_allow",
            "score": 1.0
        }
