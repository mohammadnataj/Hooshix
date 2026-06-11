"""
Test suite for Hooshix Agent Runtime
Run: python -m pytest tests/test_nexara.py -v
"""

import pytest
from nexara.memory.memory_store import MemoryStore
from nexara.core.agent_state import AgentState
from nexara.core.agent_runtime import AgentRuntime
from nexara.llm.llm_client import LLMClient
from nexara.explain.explain_engine import ExplainabilityEngine


class TestMemoryStore:
    """Test memory system"""

    def test_add_memory(self):
        memory = MemoryStore()
        memory.add_memory("Test message", metadata={"type": "test"})
        
        assert len(memory.memories) == 1
        assert memory.memories[0].content == "Test message"

    def test_search_memory(self):
        memory = MemoryStore()
        memory.add_memory("Hello world")
        memory.add_memory("Goodbye world")
        
        results = memory.search_memory("hello")
        assert len(results) == 1
        assert "Hello world" in results[0]["content"]

    def test_get_all_memories(self):
        memory = MemoryStore()
        memory.add_memory("Message 1")
        memory.add_memory("Message 2")
        
        all_mem = memory.get_all_memories()
        assert len(all_mem) == 2


class TestAgentState:
    """Test agent state management"""

    def test_initial_state(self):
        state = AgentState()
        
        assert state.trust == 0.5
        assert state.familiarity == 0.0
        assert state.emotion == "neutral"
        assert state.name == "Hooshix"

    def test_update_trust(self):
        state = AgentState()
        state.update_trust(0.1)
        
        assert state.trust == 0.6

    def test_trust_bounds(self):
        state = AgentState()
        state.update_trust(10.0)  # Try to exceed max
        
        assert state.trust == 1.0  # Should be clamped

    def test_set_emotion(self):
        state = AgentState()
        state.set_emotion("happy", 0.8)
        
        assert state.emotion == "happy"
        assert state.emotion_intensity == 0.8

    def test_apply_event_positive(self):
        state = AgentState()
        initial_trust = state.trust
        
        state.apply_event("positive_interaction")
        
        assert state.trust > initial_trust
        assert state.emotion == "happy"

    def test_apply_event_negative(self):
        state = AgentState()
        state.apply_event("negative_interaction")
        
        assert state.is_guarded == True
        assert state.emotion == "fearful"

    def test_state_to_dict(self):
        state = AgentState()
        state_dict = state.to_dict()
        
        assert "trust" in state_dict
        assert "emotion" in state_dict
        assert "familiarity" in state_dict


class TestLLMClient:
    """Test LLM integration"""

    def test_mock_provider(self):
        llm = LLMClient(provider="mock")
        response = llm.generate("test prompt")
        
        assert isinstance(response, str)
        assert len(response) > 0

    def test_mock_with_trust_keyword(self):
        llm = LLMClient(provider="mock")
        response = llm.generate("what about trust levels?")
        
        assert "trust" in response.lower()

    def test_mock_with_emotion_keyword(self):
        llm = LLMClient(provider="mock")
        response = llm.generate("how are your emotions?")
        
        assert "emotion" in response.lower()


class TestAgentRuntime:
    """Test core runtime"""

    def test_runtime_initialization(self):
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        assert runtime.memory is not None
        assert runtime.state is not None
        assert runtime.llm is not None

    def test_process_input_basic(self):
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        result = runtime.process_input("user_1", "Hello!")
        
        assert "response" in result
        assert "state" in result
        assert "memory_count" in result
        assert result["memory_count"] >= 2  # user + agent

    def test_process_input_positive_feedback(self):
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        initial_trust = state.trust
        result = runtime.process_input("user_1", "Great job! I like you!")
        
        # State should reflect positive interaction
        updated_state = result["state"]
        assert updated_state["trust"] > initial_trust
        assert updated_state["emotion"] == "happy"

    def test_process_input_negative_feedback(self):
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        result = runtime.process_input("user_1", "I hate this! You're stupid!")
        
        updated_state = result["state"]
        assert updated_state["is_guarded"] == True
        assert updated_state["emotion"] == "fearful"

    def test_multiple_interactions(self):
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        # Multiple interactions
        runtime.process_input("user_1", "Hello")
        runtime.process_input("user_1", "How are you?")
        runtime.process_input("user_1", "Nice to meet you!")
        
        # Memory should accumulate
        assert len(memory.memories) >= 6  # 3 user + 3 agent messages


class TestExplainabilityEngine:
    """Test decision explanation"""

    def test_log_decision(self):
        engine = ExplainabilityEngine()
        
        engine.log_decision(
            user_input="test",
            prompt="test prompt",
            memory_used=[],
            state_snapshot={"trust": 0.5},
            response="test response"
        )
        
        assert len(engine.logs) == 1

    def test_generate_reason_low_trust(self):
        engine = ExplainabilityEngine()
        state = {"trust": 0.2, "emotion": "neutral", "is_guarded": False}
        
        reasons = engine._generate_reason(state, [])
        
        assert any("trust" in r.lower() for r in reasons)

    def test_generate_reason_with_memory(self):
        engine = ExplainabilityEngine()
        state = {"trust": 0.5, "emotion": "neutral", "is_guarded": False}
        memory = [{"content": "test"}]
        
        reasons = engine._generate_reason(state, memory)
        
        assert any("memory" in r.lower() for r in reasons)

    def test_get_logs(self):
        engine = ExplainabilityEngine()
        
        engine.log_decision("input", "prompt", [], {}, "response")
        logs = engine.get_logs()
        
        assert len(logs) == 1
        assert "reasoning" in logs[0]


class TestFullIntegration:
    """End-to-end integration tests"""

    def test_complete_agent_flow(self):
        """Test complete agent interaction flow"""
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        explain = ExplainabilityEngine()
        
        # Simulate user interaction
        messages = [
            "Hello! Nice to meet you.",
            "How do you remember things?",
            "Thanks for helping!"
        ]
        
        for msg in messages:
            result = runtime.process_input("user_1", msg)
            
            # Log for explainability
            explain.log_decision(
                user_input=msg,
                prompt="",
                memory_used=memory.get_all_memories(),
                state_snapshot=result["state"],
                response=result["response"]
            )
        
        # Verify flow
        assert len(memory.memories) == len(messages) * 2  # user + agent
        assert len(explain.logs) == len(messages)
        
        # Verify state changed
        final_state = result["state"]
        assert final_state["trust"] > 0.5  # Should improve with positive messages

    def test_agent_learns_from_interactions(self):
        """Test that agent state evolves over time"""
        memory = MemoryStore()
        state = AgentState()
        llm = LLMClient(provider="mock")
        runtime = AgentRuntime(memory, state, llm)
        
        initial_trust = state.trust
        
        # Good interactions
        runtime.process_input("user_1", "Good job!")
        runtime.process_input("user_1", "Great work!")
        runtime.process_input("user_1", "Nice!")
        
        final_trust = state.trust
        
        # Trust should increase
        assert final_trust > initial_trust
        print(f"✅ Trust increased from {initial_trust} to {final_trust}")


# =====================================================
# PYTEST FIXTURES
# =====================================================

@pytest.fixture
def memory():
    return MemoryStore()

@pytest.fixture
def state():
    return AgentState()

@pytest.fixture
def llm():
    return LLMClient(provider="mock")

@pytest.fixture
def runtime(memory, state, llm):
    return AgentRuntime(memory, state, llm)


if __name__ == "__main__":
    # Simple run without pytest
    print("🚀 Running Hooshix Tests...\n")
    
    # Test 1: Memory
    print("📚 Test 1: Memory Store")
    memory = MemoryStore()
    memory.add_memory("Hello world")
    print(f"✅ Added memory: {len(memory.memories)} items\n")
    
    # Test 2: State
    print("🧠 Test 2: Agent State")
    state = AgentState()
    print(f"✅ Initial Trust: {state.trust}")
    state.apply_event("positive_interaction")
    print(f"✅ After positive event - Trust: {state.trust}, Emotion: {state.emotion}\n")
    
    # Test 3: LLM
    print("🤖 Test 3: LLM Client")
    llm = LLMClient(provider="mock")
    response = llm.generate("Hello LLM")
    print(f"✅ LLM Response: {response}\n")
    
    # Test 4: Runtime
    print("⚙️ Test 4: Agent Runtime")
    memory = MemoryStore()
    state = AgentState()
    llm = LLMClient(provider="mock")
    runtime = AgentRuntime(memory, state, llm)
    result = runtime.process_input("user_1", "Hello Hooshix!")
    print(f"✅ Response: {result['response']}")
    print(f"✅ Memory count: {result['memory_count']}")
    print(f"✅ Current emotion: {result['state']['emotion']}\n")
    
    # Test 5: Explainability
    print("🔍 Test 5: Explainability Engine")
    explain = ExplainabilityEngine()
    explain.log_decision("Hello", "prompt", [], result["state"], "Response")
    logs = explain.get_logs()
    print(f"✅ Logged decisions: {len(logs)}")
    print(f"✅ Reasoning: {logs[0]['reasoning']}\n")
    
    print("🎉 All tests passed!")
