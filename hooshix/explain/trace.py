import time
from typing import Dict, Any, List


class ExplainTrace:
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []

    def log(self, trace: Dict[str, Any]):
        trace["timestamp"] = time.time()
        self.traces.append(trace)

    def get_all(self):
        return self.traces

    def clear(self):
        self.traces = []
