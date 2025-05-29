from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Chat</title>
    <style>
        body {
            font-family: Arial;
            padding: 10px;
        }
        #chat-box {
            height: 70vh;
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .input-area {
            display: flex;
        }
        #message-input {
            flex-grow: 1;
            padding: 8px;
        }
        button {
            padding: 8px 15px;
        }
    </style>
</head>
<body>
    <h1>Mini Chat Đơn Giản</h1>
    <div id="chat-box"></div>
    <div class="input-area">
        <input type="text" id="message-input" placeholder="Viết tin nhắn...">
        <button onclick="sendMessage()">Gửi</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        const chatBox = document.getElementById('chat-box');
        const input = document.getElementById('message-input');
        
        function sendMessage() {
            const message = input.value.trim();
            if (message) {
                socket.emit('message', message);
                input.value = '';
            }
        }
        
        socket.on('message', msg => {
            const msgElement = document.createElement('div');
            msgElement.textContent = msg;
            chatBox.appendChild(msgElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        });
        
        input.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html)

@socketio.on('message')
def handle_message(msg):
    socketio.emit('message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
