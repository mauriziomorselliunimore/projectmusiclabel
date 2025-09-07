function sendQuickMessage() {
    const form = document.getElementById('quick-message-form');
    const messageText = document.getElementById('quick-message-text').value;
    const messageType = document.getElementById('quick-message-type').value;
    const messageSubject = document.getElementById('quick-message-subject').value;
    
    if (!messageText.trim()) {
        showNotification('Per favore inserisci un messaggio', 'danger');
        return;
    }

    // Get recipient ID from the modal
    const recipientId = form.dataset.recipientId;
    
    // Show loading state
    const sendBtn = document.querySelector('#quickMessageModal .btn-success');
    const originalBtnText = sendBtn.innerHTML;
    sendBtn.innerHTML = '<i class="bi bi-hourglass"></i> Invio...';
    sendBtn.disabled = true;

    // Send message via API
    fetch('/messaging/api/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            recipient_id: recipientId,
            content: messageText,
            subject: messageSubject || 'Messaggio Rapido',
            message_type: messageType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('quickMessageModal'));
            modal.hide();
            
            // Show success message
            showNotification('Messaggio inviato con successo!', 'success');
            
            // Reset form
            form.reset();
            
            // Optionally redirect to conversation
            if (data.conversation_url) {
                setTimeout(() => {
                    window.location.href = data.conversation_url;
                }, 1500);
            }
        } else {
            throw new Error(data.error || 'Errore nell\'invio del messaggio');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification(error.message || 'Errore nell\'invio del messaggio', 'danger');
    })
    .finally(() => {
        // Reset button state
        sendBtn.innerHTML = originalBtnText;
        sendBtn.disabled = false;
    });
}

function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Initialize Bootstrap alert
    const bsAlert = new bootstrap.Alert(notification);
    
    // Auto dismiss after duration
    setTimeout(() => {
        bsAlert.close();
    }, duration);
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Initialize message modal with recipient data
function initQuickMessage(recipientId, recipientName) {
    const form = document.getElementById('quick-message-form');
    const recipientNameEl = document.getElementById('recipient-name');
    
    form.dataset.recipientId = recipientId;
    recipientNameEl.textContent = recipientName;
    
    // Reset form
    form.reset();
}
