from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from hooshix.core.agent_runtime import AgentRuntime
from hooshix.memory.memory_store import MemoryStore
from hooshix.core.agent_state import AgentState
from hooshix.llm.llm_client import LLMClient


memory = MemoryStore()
state = AgentState()
llm = LLMClient()
agent = AgentRuntime(memory, state, llm)


class Handler(BaseHTTPRequestHandler):

    def _send(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/health":
            self._send({"status": "ok", "service": "hooshix-light"})
        else:
            self._send({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/run":
            length = int(self.headers.get('Content-Length'))
            body = json.loads(self.rfile.read(length))

            result = agent.process_input(
                body.get("user_id", ""),
                body.get("message", "")
            )

            self._send(result)
        else:
            self._send({"error": "not found"}, 404)


def run():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("🚀 Hooshix Light Server running on 8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
