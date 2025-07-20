function toggleMenu() {
    const menu = document.getElementById('dropdownMenu');
    menu.classList.toggle('show');
}

function showUserInfo() {
    fetch('/userinfo')
        .then(res => res.json())
        .then(data => {
            document.getElementById('extra-content').innerHTML = `
                <h3>User Info</h3>
                <p>Email: ${data.email}</p>
            `;
            showExtra();
        });
}

function showFeedbackForm() {
    document.getElementById('extra-content').innerHTML = `
        <h3>Send Feedback</h3>
        <textarea id="feedback-text" rows="4" cols="50" placeholder="Enter your feedback..."></textarea><br/>
        <button onclick="submitFeedback()">Submit</button>
    `;
    showExtra();
}

function showAbout() {
    document.getElementById('extra-content').innerHTML = `
        <h3>About Nexture AI</h3>
        <p>Nexture AI is your personal AI assistant for productivity, writing, task management, and more.</p>
    `;
    showExtra();
}

function toggleTheme() {
    document.body.classList.toggle('dark');
}

function showExtra() {
    document.getElementById('extra-content').classList.remove('hidden');
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += <div class="user-msg">You: ${message}</div>;
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += <div class="bot-msg">Bot: ${data.response}</div>;
    });
}