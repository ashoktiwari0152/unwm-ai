async function sendPrompt() {

    const input = document.getElementById("user-input").value;

    const result = document.getElementById("result");

    result.innerHTML = "Loading...";

    try {

        const response = await fetch("https://secure-elegance-production-4e74.up.railway.app/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: input,
                depth: "normal"
            })

        });

        const data = await response.json();

        console.log(data);

        result.innerHTML = `

            <h2>AI Response</h2>
            <p>${data.response}</p>

            <h2>Recursive Analysis</h2>
            <pre>${JSON.stringify(data.recursives_analysis, null, 2)}</pre>

        `;

    } catch (error) {

        console.error(error);

        result.innerHTML = "Server Error";

    }

}
