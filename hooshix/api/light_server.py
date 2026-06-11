import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from hooshix.core.agent_runtime import AgentRuntime
from hooshix.memory.memory_store import MemoryStore
from hooshix.core.agent_state import AgentState
from hooshix.llm.llm_client import LLMClient


# -------------------------
# 🧠 INIT CORE ENGINE
# -------------------------
memory = MemoryStore()
state = AgentState()
llm = LLMClient()

agent = AgentRuntime(
    memory=memory,
    state=state,
    llm=llm
)


# -------------------------
# 🌐 LIGHT HTTP SERVER
# -------------------------
class HooshixHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # -------------------------
    # HEALTH CHECK
    # -------------------------
    def do_GET(self):
        if self.path == "/health":
            return self._send_json({
                "status": "ok",
                "system": "hooshix-light-api"
            })

        if self.path == "/state":
            return self._send_json(state.to_dict())

        return self._send_json({
            "error": "not found"
        }, 404)

    # -------------------------
    # MAIN RUN ENDPOINT
    # -------------------------
    def do_POST(self):
        if self.path != "/run":
            return self._send_json({"error": "not found"}, 404)

        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)

            user_id = data.get("user_id", "unknown")
            message = data.get("message", "")

            result = agent.process_input(
                user_id=user_id,
                message=message
            )

            return self._send_json(result)

        except Exception as e:
            return self._send_json({
                "error": str(e)
            }, 500)


# -------------------------
# 🚀 RUN SERVER
# -------------------------
def run_server(host="0.0.0.0", port=8000):
    server = HTTPServer((host, port), HooshixHandler)
    print(f"🚀 Hooshix Light API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
