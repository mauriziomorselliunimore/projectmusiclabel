from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# Frontend WebSocket JavaScript
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    if (data.type === 'chat_message') {
        displayMessage(data);
    } else if (data.type === 'typing') {
        showTypingIndicator(data);
    }
};

function sendMessage(message, recipientId) {
    chatSocket.send(JSON.stringify({
        'type': 'chat_message',
        'message': message,
        'recipient_id': recipientId
    }));
}

function sendTypingIndicator(isTyping) {
    chatSocket.send(JSON.stringify({
        'type': 'typing',
        'is_typing': isTyping
    }));
}