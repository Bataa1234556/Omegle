document.addEventListener('DOMContentLoaded', function () {
    const roomName = document.getElementById('room-name').textContent;
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const chatLog = document.getElementById('chat-log');
        chatLog.value += data.message + '\n';
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.getElementById('chat-message-submit').onclick = function () {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value;

        if (message.trim()) { // Prevent sending empty messages
            chatSocket.send(JSON.stringify({ message: message }));
            messageInput.value = '';
        }
    };
});


