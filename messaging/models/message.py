from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Message(models.Model):
    """Rappresenta un singolo messaggio"""
    MESSAGE_TYPES = [
        ('general', 'Messaggio Generale'),
        ('booking_request', 'Richiesta Prenotazione'),
        ('collaboration', 'Proposta Collaborazione'),
        ('inquiry', 'Richiesta Informazioni'),
        ('quote_request', 'Richiesta Preventivo'),
        ('other', 'Altro'),
    ]
    
    conversation = models.ForeignKey(
        'messaging.Conversation', 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    # Contenuto messaggio
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(default='')  # Campo message con valore di default
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Collegamenti opzionali
    related_booking = models.ForeignKey(
        'booking.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.subject or self.message[:50]}..."
    
    def mark_as_read(self):
        """Segna il messaggio come letto"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    def get_absolute_url(self):
        return reverse('messaging:conversation', kwargs={'conversation_id': self.conversation.pk})
    
    @property
    def is_recent(self):
        """Controlla se il messaggio è stato inviato nelle ultime 24 ore"""
        return (timezone.now() - self.created_at).total_seconds() < 86400
    
    def save(self, *args, **kwargs):
        # Assicurati che il recipient sia corretto
        if not self.recipient:
            self.recipient = self.conversation.get_other_participant(self.sender)
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Aggiorna la conversazione se è un nuovo messaggio
        if is_new:
            self.conversation.update_last_message(self)
