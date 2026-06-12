from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from hooshix.core.agent_runtime import AgentRuntime
from hooshix.memory.memory_store import MemoryStore
from hooshix.core.agent_state import AgentState
from hooshix.llm.llm_client import LLMClient

app = FastAPI(title="Hooshix API", version="0.2")

# -------------------------
# Simple API Key (MVP level)
# -------------------------
API_KEY = "hooshix-dev-key"

def verify_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# -------------------------
# Request Schema
# -------------------------
class RunRequest(BaseModel):
    user_id: str
    message: str

# -------------------------
# Runtime Init (singleton)
# -------------------------
runtime = AgentRuntime(
    memory=MemoryStore(),
    state=AgentState(),
    llm=LLMClient()
)

# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Hooshix API v0.2"
    }

# -------------------------
# Main Execution Endpoint
# -------------------------
@app.post("/run")
def run(req: RunRequest, x_api_key: str = Header(None)):
    verify_key(x_api_key)

    result = runtime.process_input(req.user_id, req.message)

    return {
        "success": True,
        "result": result
    }
