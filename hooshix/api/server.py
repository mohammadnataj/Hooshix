from hooshix.core.agent_runtime import AgentRuntime
from hooshix.memory.memory_store import MemoryStore
from hooshix.core.agent_state import AgentState
from hooshix.llm.llm_client import LLMClient

# --- initialize runtime ---
runtime = AgentRuntime(
    memory=MemoryStore(),
    state=AgentState(),
    llm=LLMClient()
)

def run(user_id, message):
    """
    Real Hooshix API → runtime pipeline
    """
    result = runtime.process_input(user_id, message)

    return {
        "response": result["response"],
        "state": result["state"],
        "memory_count": result["memory_count"],
        "reasoning": result.get("reasoning", [])
    }
