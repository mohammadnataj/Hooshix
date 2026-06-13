# 🧠 Hooshix

**A Lightweight AI Agent Runtime with Policy, Memory, and Explainability**

Hooshix is an open-source AI Agent Runtime framework that allows developers and companies to build **controllable, stateful, and observable AI agents**.

It is designed for:
- AI applications
- Game NPC systems
- Automation agents
- Enterprise AI workflows

---

# 🚀 What Hooshix Does

Hooshix runs AI agents through a controlled execution pipeline:

User Input  
→ Policy Engine (control & safety)  
→ Memory System (context awareness)  
→ Agent State (behavior tracking)  
→ LLM Processing  
→ Explainability Trace  
→ Response Output  

---

# 🧠 Core Features

## ⚖️ Policy Engine
Controls AI behavior before execution:
- ALLOW → execute request
- MODIFY → adjust input
- BLOCK → reject unsafe input

---

## 💾 Memory System
Stores and retrieves context for agents:
- conversation history
- user context
- runtime memory state

---

## ⚙️ Agent State
Tracks internal agent behavior:
- trust score
- familiarity level
- emotional state (basic simulation)

---

## 🔍 Explainability Engine
Every decision is traceable:
- why input was modified
- why request was blocked
- how response was generated

---

## 🌐 API Layer
Hooshix exposes a simple runtime API for external systems.

---

# 🏗️ Architecture

User 
↓ 
Policy Engine 
↓ 
Memory System 
↓ 
Agent State 
↓ 
LLM Client 
↓ 
Explainability Trace 
↓ 
Response

---

# 🚀 Quick Start (5–10 Minutes)

## 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/Hooshix.git
cd Hooshix

pip install -r requirements.txt

Install dependencies
Bash
pip install -r requirements.txt
3. Run server
Bash
python run.py
🌐 API Test
Health Check
Bash
curl http://127.0.0.1:8000/health
Expected response:
JSON
{
  "status": "ok",
  "system": "hooshix runtime active"
}
Run Agent
Bash
curl -X POST http://127.0.0.1:8000/run \
-H "Content-Type: application/json" \
-d '{
  "user_id": "demo",
  "message": "hello hooshix"
}'
System Check
Bash
python -m hooshix.tools.system_check
Expected:

✔ Runtime Engine: OK
✔ Policy Engine: OK
✔ Memory Store: OK
✔ Explainability: OK
✔ API Server: OK
📌 Use Cases
AI Agent platforms
Game NPC intelligence systems
Customer support automation
Workflow AI systems
Research AI frameworks
⚠️ Status
Hooshix is currently in MVP stage:
Core runtime is stable
API layer is functional
Memory and policy systems are active
Not yet production-ready for enterprise scale.
🧭 Roadmap
v0.1 ✔
Runtime engine
Policy system
Memory system
Trace system
v0.2 🚧
API improvements
Authentication
Logging system
v0.3
Multi-agent runtime
Plugin system
Tool execution layer
🧠 Philosophy
Control over chaos
Explainability over opacity
Stateful AI over stateless prompts
Governance over raw generation
👤 Author
Mohammad Hassan Nataj Ansar