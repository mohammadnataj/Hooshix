class PolicyDecision:
    ALLOW = "allow"
    MODIFY = "modify"
    BLOCK = "block"


class PolicyEngine:
    def __init__(self, rules=None):
        self.rules = rules or []

    def evaluate(self, input_text, state=None):
        for rule in self.rules:
            result = rule.apply(input_text, state)

            if result == PolicyDecision.BLOCK:
                return {
                    "decision": "block",
                    "reason": rule.name
                }

            if result == PolicyDecision.MODIFY:
                return {
                    "decision": "modify",
                    "input": rule.modify(input_text),
                    "reason": rule.name
                }

        return {
            "decision": "allow",
            "input": input_text
        }
