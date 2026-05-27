const API_URL =
"https://secure-elegance-production-4e74.up.railway.app/generate";

const sendBtn =
document.getElementById("send-btn");

const userInput =
document.getElementById("user-input");

const chatBox =
document.getElementById("chat-box");

sendBtn.onclick = sendMessage;

async function sendMessage() {

    const message = userInput.value;

    if (!message) {
        return;
    }

    chatBox.innerHTML = "Thinking...";

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: message,
                depth: "deep"
            })
        });

        const data = await response.json();

        let patternsHTML = "";

        if (
            data.recursives_analysis &&
            data.recursives_analysis.patterns_detected
        ) {

            for (
                let i = 0;
                i < data.recursives_analysis.patterns_detected.length;
                i++
            ) {

                patternsHTML +=
                    "<li>" +
                    data.recursives_analysis.patterns_detected[i] +
                    "</li>";
            }
        }

        let recursiveHTML = "";

        if (data.recursives_analysis) {

            recursiveHTML =

            "<h2>Recursive Analysis</h2>" +

            "<p><b>State:</b> " +
            data.recursives_analysis.recursive_state +
            "</p>" +

            "<p><b>Collapse Risk:</b> " +
            data.recursives_analysis.collapse_risk +
            "</p>" +

            "<p><b>Stability Index:</b> " +
            data.recursives_analysis.stability_index +
            "</p>" +

            "<p><b>Recursive Density:</b> " +
            data.recursives_analysis.recursive_density +
            "</p>" +

            "<h3>Patterns</h3>" +

            "<ul>" +
            patternsHTML +
            "</ul>";
        }

        chatBox.innerHTML =

            "<h2>AI Response</h2>" +

            "<p>" +
            data.response +
            "</p>" +

            recursiveHTML;

    }

    catch (error) {

        console.log(error);

        chatBox.innerHTML =
            "<p>Server Error</p>";
    }
}
