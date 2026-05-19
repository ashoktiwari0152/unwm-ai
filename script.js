const API_URL = "https://unwm-ai1.onrender.com";

const inputBox = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const historyBox = document.getElementById("history-box");

let chats = JSON.parse(localStorage.getItem("unwm_chats")) || [];

renderHistory();

function saveChats() {
    localStorage.setItem(
        "unwm_chats",
        JSON.stringify(chats)
    );
}

function renderHistory() {

    historyBox.innerHTML = "";

    chats.forEach((chat) => {

        const div = document.createElement("div");

        div.className = "history-item";

        div.innerText = chat.user;

        div.onclick = () => {

            chatBox.innerHTML = "";

            addMessage(chat.user, "user-message");

            addMessage(chat.bot, "bot-message");
        };

        historyBox.appendChild(div);
    });
}

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
                depth: "normal"
            })
        });

        const data = await response.json();

        const botReply = data.response;

        addMessage(botReply, "bot-message");

        chats.push({
            user: message,
            bot: botReply
        });

        saveChats();

        renderHistory();

    } catch (error) {

        addMessage(
            "Server Error",
            "bot-message"
        );

        console.error(error);
    }
}

sendBtn.addEventListener(
    "click",
    sendMessage
);

inputBox.addEventListener(
    "keypress",
    function (e) {

        if (e.key === "Enter") {

            sendMessage();
        }
    }
);
