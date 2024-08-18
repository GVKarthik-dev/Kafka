let token = '';

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('http://localhost:8000/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        token = data.access_token;
        document.getElementById("login").style.display = "none";
        document.getElementById("chat").style.display = "block";
        getMessages();
    })
    .catch(error => console.error('Error:', error));
}

function getMessages() {
    fetch('http://localhost:8000/messages/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(messages => {
        const messagesDiv = document.getElementById("messages");
        messagesDiv.innerHTML = '';
        messages.forEach(message => {
            const messageElement = document.createElement("div");
            messageElement.textContent = message.content;
            if (!message.is_read) {
                messageElement.style.fontWeight = "bold";
            }
            messagesDiv.appendChild(messageElement);
        });
    })
    .catch(error => console.error('Error:', error));
}

function sendMessage() {
    const messageInput = document.getElementById("message-input").value;

    fetch('http://localhost:8000/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            content: messageInput,
            receiver_id: 2  // Assume the receiver ID for demo purposes
        })
    })
    .then(response => response.json())
    .then(data => {
        getMessages();
    })
    .catch(error => console.error('Error:', error));
}
