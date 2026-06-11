const API_URL = "http://127.0.0.1:8000/chat";

async function sendMessage() {
    const input = document.getElementById("input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value;
    if (!message) return;

    // نمایش پیام کاربر
    chatBox.innerHTML += `<div class="user">🧑 You: ${message}</div>`;

    input.value = "";

    // ارسال به API
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "demo_user",
                message: message
            })
        });

        const data = await response.json();

        // نمایش پاسخ Agent
        chatBox.innerHTML += `<div class="agent">🧠 Hooshix: ${data.response}</div>`;

        // نمایش state
        document.getElementById("state").innerText =
            JSON.stringify(data.state, null, 2);

        // (فعلاً explainability نداریم در API، بعداً اضافه می‌کنیم)

    } catch (error) {
        chatBox.innerHTML += `<div class="error">❌ Error connecting to API</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}