Hooshix Memory Demo

This demo shows how Hooshix retains context across interactions.

---

Step 1: Store Information

Request:

POST /run

{
"user_id": "user1",
"message": "My name is Ali"
}

---

Step 2: Query Memory

Request:

POST /run

{
"user_id": "user1",
"message": "What is my name?"
}

---

Expected Behavior

Hooshix should respond using stored memory, such as:

"Your name is Ali"

---

Key Feature

Unlike stateless LLM APIs, Hooshix maintains:

- Persistent memory
- Agent state
- Traceable reasoning
