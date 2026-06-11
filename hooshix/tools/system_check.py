from hooshix.core.agent_runtime import AgentRuntime
from hooshix.core.agent_state import AgentState
from hooshix.memory.memory_store import MemoryStore
from hooshix.llm.llm_client import LLMClient
from hooshix.policy.policy_engine import PolicyEngine
from hooshix.explain.trace import ExplainTrace


def system_check():
    print("\n🧠 HOOSHIX SYSTEM HEALTH CHECK\n")

    results = {}

    # ---------------- CORE ----------------
    try:
        runtime = AgentRuntime(
            memory=MemoryStore(),
            state=AgentState(),
            llm=LLMClient()
        )
        results["runtime"] = "OK"
    except Exception as e:
        results["runtime"] = str(e)

    # ---------------- POLICY ----------------
    try:
        engine = PolicyEngine()
        results["policy"] = "OK"
    except Exception as e:
        results["policy"] = str(e)

    # ---------------- TRACE ----------------
    try:
        trace = ExplainTrace()
        trace.add({"test": "ok"})
        results["trace"] = "OK"
    except Exception as e:
        results["trace"] = str(e)

    # ---------------- MEMORY ----------------
    try:
        runtime.memory.add_memory(
            content="health check",
            metadata={"test": True}
        )
        results["memory"] = "OK"
    except Exception as e:
        results["memory"] = str(e)

    # ---------------- PIPELINE TEST ----------------
    try:
        response = runtime.process_input(
            user_id="health",
            message="hello system"
        )
        results["pipeline"] = "OK"
        results["sample_response"] = response["response"]
    except Exception as e:
        results["pipeline"] = str(e)

    # ---------------- REPORT ----------------
    print("\n📊 RESULTS:\n")
    for k, v in results.items():
        print(f"{k}: {v}")

    print("\n✅ SYSTEM CHECK COMPLETE\n")


if __name__ == "__main__":
    system_check()
