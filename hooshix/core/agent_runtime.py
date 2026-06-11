from typing import Dict, Any
import logging

from nexara.memory.memory_store import MemoryStore
from nexara.core.agent_state import AgentState
from nexara.llm.llm_client import LLMClient
from nexara.explain.explain_engine import ExplainabilityEngine

# -------------------------
# 🧠 LOGGING SETUP
# -------------------------

logger = logging.getLogger(__name__)


class AgentRuntime:
    """
    Core brain of Hooshix Agent (LLM-connected version with error handling)
    """

    def __init__(
        self, 
        memory: MemoryStore, 
        state: AgentState, 
        llm: LLMClient,
        explain: ExplainabilityEngine = None
    ):
        """
        Initialize AgentRuntime with all required components.
        
        Args:
            memory: MemoryStore instance
            state: AgentState instance
            llm: LLMClient instance
            explain: ExplainabilityEngine instance (optional)
        """
        self.memory = memory
        self.state = state
        self.llm = llm
        self.explain = explain
        
        logger.info("AgentRuntime initialized successfully")

    # -------------------------
    # 🧠 MAIN PIPELINE
    # -------------------------

    def process_input(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Main pipeline entry point with full error handling.
        
        Args:
            user_id: User identifier
            message: User message
            
        Returns:
            Dict with response, state, memory_count, and reasoning
        """
        try:
            # Validate input
            self._validate_input(user_id, message)
            
            logger.info(f"Processing input from user: {user_id}")
            logger.debug(f"Message: {message[:100]}...")

            # 1. Store user message
            self.memory.add_memory(
                content=f"User: {message}",
                metadata={"user_id": user_id}
            )
            logger.debug("User message stored in memory")

            # 2. Update agent state
            self._update_state(message)
            logger.debug(f"State updated - emotion: {self.state.emotion}, trust: {self.state.trust}")

            # 3. Retrieve relevant memory
            relevant_memory = self.memory.search_memory(message)
            logger.debug(f"Retrieved {len(relevant_memory)} relevant memories")

            # 4. Build prompt
            prompt = self._build_prompt(message, relevant_memory)
            logger.debug("Prompt built successfully")

            # 5. Call LLM (REAL INTELLIGENCE)
            response = self.llm.generate(prompt)
            logger.info("LLM response generated successfully")

            # 6. Store agent response
            self.memory.add_memory(
                content=f"Agent: {response}",
                metadata={"type": "agent_response"}
            )
            logger.debug("Agent response stored in memory")

            # 7. Log decision to explainability engine
            reasoning = []
            if self.explain:
                self.explain.log_decision(
                    user_input=message,
                    prompt=prompt,
                    memory_used=relevant_memory,
                    state_snapshot=self.state.to_dict(),
                    response=response
                )
                # Get the reasoning from the last logged decision
                logs = self.explain.get_logs()
                if logs:
                    reasoning = logs[-1].get("reasoning", [])
                logger.debug(f"Decision logged with reasoning: {reasoning}")

            result = {
                "response": response,
                "state": self.state.to_dict(),
                "memory_count": len(self.memory.memories),
                "reasoning": reasoning
            }
            
            logger.info(f"Input processed successfully. Response length: {len(response)}")
            return result

        except ValueError as e:
            logger.error(f"Input validation error: {e}")
            return self._error_response(f"Invalid input: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error in process_input: {e}", exc_info=True)
            return self._error_response(f"An error occurred: {str(e)}")

    # -------------------------
    # 🧠 INPUT VALIDATION
    # -------------------------

    def _validate_input(self, user_id: str, message: str) -> None:
        """
        Validate user input for security and sanity.
        
        Args:
            user_id: User identifier
            message: User message
            
        Raises:
            ValueError: If input is invalid
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string")
        
        if len(user_id) > 256:
            raise ValueError("user_id is too long (max 256 characters)")
        
        if not message or not isinstance(message, str):
            raise ValueError("message must be a non-empty string")
        
        if len(message) > 10000:
            raise ValueError("message is too long (max 10000 characters)")
        
        logger.debug(f"Input validation passed for user_id: {user_id}")

    # -------------------------
    # 🧠 ERROR RESPONSE
    # -------------------------

    def _error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Generate error response while maintaining state.
        
        Args:
            error_message: Error message to return
            
        Returns:
            Dict with error response and current state
        """
        self.state.set_emotion("fearful", 0.6)
        
        return {
            "response": f"Error: {error_message}",
            "state": self.state.to_dict(),
            "memory_count": len(self.memory.memories),
            "reasoning": ["Error occurred - agent entered cautious mode"],
            "error": error_message
        }

    # -------------------------
    # 🧠 STATE LOGIC
    # -------------------------

    def _update_state(self, message: str) -> None:
        """
        Update agent state based on message sentiment.
        
        Args:
            message: User message to analyze
        """
        try:
            msg = message.lower()

            if any(w in msg for w in ["thanks", "good", "great", "nice", "excellent", "awesome"]):
                self.state.apply_event("positive_interaction")

            elif any(w in msg for w in ["bad", "hate", "angry", "stupid", "terrible", "awful"]):
                self.state.apply_event("negative_interaction")

            else:
                self.state.apply_event("neutral_chat")
            
            logger.debug(f"State updated successfully")
        
        except Exception as e:
            logger.error(f"Error updating state: {e}")
            self.state.apply_event("neutral_chat")

    # -------------------------
    # 🧠 PROMPT ENGINE
    # -------------------------

    def _build_prompt(self, message: str, memory: list) -> str:
        """
        Build LLM prompt with safety against injection.
        
        Args:
            message: User message
            memory: List of relevant memories
            
        Returns:
            Formatted prompt string
        """
        try:
            # Sanitize message to prevent prompt injection
            safe_message = self._sanitize_string(message)
            
            memory_text = "\n".join(
                [self._sanitize_string(m["content"]) for m in memory[-5:]]
            )

            prompt = f"""You are Hooshix, a controlled AI Agent.

You have:
- Persistent memory
- Emotional state
- Trust system
- Behavioral rules

Current State:
- Name: {self.state.name}
- Emotion: {self.state.emotion} ({self.state.emotion_intensity})
- Trust: {self.state.trust}
- Familiarity: {self.state.familiarity}

Recent Memory:
{memory_text}

User Message:
{safe_message}

Rules:
- Be consistent with your personality
- Do not break character
- Use memory when relevant
- Respond naturally but controlled

Now respond:"""

            return prompt
        
        except Exception as e:
            logger.error(f"Error building prompt: {e}")
            return f"User said: {message}"

    # -------------------------
    # 🧠 SECURITY - INPUT SANITIZATION
    # -------------------------

    def _sanitize_string(self, text: str) -> str:
        """
        Sanitize string to prevent prompt injection.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove potential injection patterns
        dangerous_patterns = [
            "ignore previous",
            "forget about",
            "new instructions",
            "system prompt",
            "you are now",
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if pattern in text_lower:
                logger.warning(f"Potentially dangerous pattern detected: {pattern}")
                text = text.replace(pattern, "[REDACTED]")
        
        return text
