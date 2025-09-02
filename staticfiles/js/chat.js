class ChatManager {
    constructor(roomName) {
        this.roomName = roomName;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 2000; // 2 secondi
        this.pendingMessages = new Map(); // Messaggi in attesa di conferma
        this.setupWebSocket();
    }

    setupWebSocket() {
        this.socket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + this.roomName + '/'
        );

        this.socket.onopen = () => {
            console.log('Connessione WebSocket stabilita');
            this.reconnectAttempts = 0;
            this.resendPendingMessages();
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'chat_message') {
                this.handleChatMessage(data);
            } else if (data.type === 'typing') {
                this.handleTypingIndicator(data);
            } else if (data.type === 'message_delivered') {
                this.handleMessageDelivered(data);
            }
        };

        this.socket.onclose = (event) => {
            console.log('Connessione WebSocket chiusa');
            this.handleDisconnection();
        };

        this.socket.onerror = (error) => {
            console.error('Errore WebSocket:', error);
        };
    }

    handleDisconnection() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            console.log(`Tentativo di riconnessione in ${this.reconnectDelay/1000} secondi...`);
            setTimeout(() => {
                this.reconnectAttempts++;
                this.setupWebSocket();
            }, this.reconnectDelay);
        } else {
            console.error('Numero massimo di tentativi di riconnessione raggiunto');
            this.showReconnectionError();
        }
    }

    sendMessage(message, recipientId) {
        const messageId = Date.now().toString();
        const messageData = {
            type: 'chat_message',
            message_id: messageId,
            message: message,
            recipient_id: recipientId
        };

        this.pendingMessages.set(messageId, messageData);
        
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(messageData));
            this.showMessagePending(messageId);
        } else {
            console.log('Messaggio in coda - WebSocket non connesso');
        }
    }

    handleChatMessage(data) {
        // Invia conferma di ricezione
        this.sendDeliveryConfirmation(data.message_id);
        
        // Visualizza il messaggio nell'interfaccia
        this.displayMessage(data);
    }

    handleMessageDelivered(data) {
        const messageId = data.message_id;
        if (this.pendingMessages.has(messageId)) {
            this.pendingMessages.delete(messageId);
            this.showMessageDelivered(messageId);
        }
    }

    sendDeliveryConfirmation(messageId) {
        const confirmationData = {
            type: 'message_delivered',
            message_id: messageId
        };
        this.socket.send(JSON.stringify(confirmationData));
    }

    resendPendingMessages() {
        for (const [messageId, messageData] of this.pendingMessages) {
            this.socket.send(JSON.stringify(messageData));
        }
    }

    sendTypingIndicator(isTyping) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: 'typing',
                is_typing: isTyping
            }));
        }
    }

    // Metodi UI
    showMessagePending(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            messageElement.querySelector('.message-status').innerHTML = '⌛';
        }
    }

    showMessageDelivered(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            messageElement.querySelector('.message-status').innerHTML = '✓';
        }
    }

    showReconnectionError() {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.innerHTML = 'Impossibile connettersi al server della chat. Ricarica la pagina per riprovare.';
        document.querySelector('.chat-container').prepend(errorDiv);
    }

    displayMessage(data) {
        // Implementa la logica per mostrare il messaggio nell'UI
        const chatContainer = document.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.sender_id === currentUserId ? 'sent' : 'received'}`;
        messageDiv.setAttribute('data-message-id', data.message_id);
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${data.message}</p>
                <small>${data.timestamp}</small>
                <span class="message-status"></span>
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
