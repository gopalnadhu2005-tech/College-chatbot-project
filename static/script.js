const input = document.getElementById("message");


// Press Enter to send
input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});


// Quick question buttons
function quickQuestion(question) {

    input.value = question;

    sendMessage();

}


// Add message to chat
function addMessage(message, type) {

    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");

    messageDiv.className = "message " + type;


    const avatar = document.createElement("div");

    avatar.className = "avatar";

    if (type === "user") {
        avatar.innerText = "👤";
    } else {
        avatar.innerText = "🤖";
    }


    const content = document.createElement("div");

    content.className = "message-content";


    const name = document.createElement("div");

    name.className = "name";

    if (type === "user") {
        name.innerText = "You";
    } else {
        name.innerText = "CollegeBot";
    }


    const bubble = document.createElement("div");

    bubble.className = "bubble";

    bubble.innerText = message;


    content.appendChild(name);

    content.appendChild(bubble);

    messageDiv.appendChild(avatar);

    messageDiv.appendChild(content);

    chatBox.appendChild(messageDiv);


    chatBox.scrollTop = chatBox.scrollHeight;
}


// Send question to Flask
async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }


    // Show user message
    addMessage(message, "user");

    input.value = "";


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        // Show chatbot answer
        addMessage(data.answer, "bot");


    } catch (error) {

        addMessage(
            "Sorry, I could not connect to the server.",
            "bot"
        );

    }

}