Hooshix API

Health Check

Request

GET /health

Response

{
"status": "ok",
"service": "hooshix-light"
}

---

Run Agent

Request

POST /run

{
"user_id": "test",
"message": "hello"
}

Response

{
"response": "...",
"state": {...},
"memory_count": 1,
"trace": [...]
}
