class ExplainTrace:
    """
    Simple trace system for Hooshix runtime
    """

    def __init__(self):
        self.traces = []

    def add(self, trace: dict):
        self.traces.append(trace)

    def log(self, trace: dict):
        self.traces.append(trace)

    def get_all(self):
        return self.traces
