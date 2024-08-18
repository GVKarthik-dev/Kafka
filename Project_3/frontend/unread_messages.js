window.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login.html';
    }

    const response = await fetch('/messages/unread', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    const messagesDiv = document.getElementById('messages');

    if (data.unread_messages.length > 0) {
        data.unread_messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            messageDiv.textContent = `${message.content} - Sentiment: ${message.sentiment}`;
            messagesDiv.appendChild(messageDiv);
        });
    } else {
        messagesDiv.textContent = 'No unread messages.';
    }
});
