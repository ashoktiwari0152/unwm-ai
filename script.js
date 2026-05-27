const API_URL = "secure-elegance-production-4e74.up.railway.app";

const inputBox = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");

function addMessage(text, className) {

    const div = document.createElement("div");

    div.className = className;

    div.innerText = text;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {

    const message = inputBox.value.trim();

    if (!message) return;

    addMessage(message, "user-message");

    inputBox.value = "";

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: message,
                depth: "medium"
            })
        });

        const data = await response.json();

        console.log(data);

        const botReply =
            data.response ||
            data.reply ||
            data.message ||
            JSON.stringify(data);

        addMessage(botReply, "bot-message");

    } catch (error) {

        console.log(error);

        addMessage("Server Error", "bot-message");
    }
}

sendBtn.addEventListener("click", sendMessage);

inputBox.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        sendMessage();
    }
});
