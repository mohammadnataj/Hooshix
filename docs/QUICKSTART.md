Quick Start Guide - Hooshix

1. Clone Project

git clone https://github.com/mohammadnataj/Hooshix.git

cd Hooshix

---

2. System Check

python -m hooshix.tools.system_check

---

3. Run Light API

python -m hooshix.api.light_server

---

4. Test API

curl http://127.0.0.1:8000/health

curl -X POST "http://127.0.0.1:8000/run" 
-H "Content-Type: application/json" 
-d '{"user_id":"test","message":"hello"}'
