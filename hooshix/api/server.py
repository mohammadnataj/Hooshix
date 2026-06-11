from fastapi import FastAPI
from pydantic import BaseModel

from nexara.memory.memory_store import MemoryStore
from nexara.core.agent_state import AgentState
from nexara.llm.llm_client import LLMClient
from nexara.explain.explain_engine import ExplainabilityEngine
from nexara.core.agent_runtime import AgentRuntime

# -------------------------
# 🚀 INIT SYSTEM
# -------------------------

app = FastAPI(title="Hooshix API", version="1.0")

memory = MemoryStore()
state = AgentState()
llm = LLMClient(provider="mock")
explain = ExplainabilityEngine()

agent = AgentRuntime(memory, state, llm, explain)

# -------------------------
# 📦 REQUEST MODEL
# -------------------------

class ChatRequest(BaseModel):
    user_id: str
    message: str

# -------------------------
# 💬 CHAT ENDPOINT
# -------------------------

@app.post("/chat")
def chat(req: ChatRequest):
    result = agent.process_input(req.user_id, req.message)

    return {
        "response": result["response"],
        "state": result["state"],
        "memory_count": result["memory_count"]
    }

# -------------------------
# 🧠 STATE ENDPOINT
# -------------------------

@app.get("/state")
def get_state():
    return state.to_dict()

# -------------------------
# 📚 MEMORY ENDPOINT
# -------------------------

@app.get("/memory")
def get_memory():
    return memory.get_all_memories()

# -------------------------
# 🔍 EXPLAINABILITY ENDPOINT
# -------------------------

@app.get("/explain")
def get_explain():
    return explain.get_logs()