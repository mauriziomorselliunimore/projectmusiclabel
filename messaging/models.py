from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    """Rappresenta una conversazione tra due utenti"""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = [p.get_full_name() or p.username for p in self.participants.all()]
        return f"Conversazione: {' - '.join(participant_names)}"
    
    def get_other_participant(self, user):
        """Ottiene l'altro partecipante della conversazione"""
        return self.participants.exclude(id=user.id).first()
    
    def get_last_message(self):
        """Ottiene l'ultimo messaggio della conversazione"""
        return self.messages.first()
    
    def has_unread_messages(self, user):
        """Controlla se ci sono messaggi non letti per l'utente"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).exists()
    
    def unread_count(self, user):
        """Conta i messaggi non letti per l'utente"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).count()


class Message(models.Model):
    """Rappresenta un singolo messaggio"""
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    def mark_as_read(self):
        """Segna il messaggio come letto"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])


class Notification(models.Model):
    """Sistema di notifiche generico"""
    NOTIFICATION_TYPES = [
        ('message', 'Nuovo Messaggio'),
        ('booking', 'Nuova Prenotazione'),
        ('booking_confirmed', 'Prenotazione Confermata'),
        ('booking_cancelled', 'Prenotazione Cancellata'),
        ('demo_feedback', 'Feedback Demo'),
        ('profile_view', 'Profilo Visualizzato'),
        ('quote_request', 'Richiesta Preventivo'),
        ('quote_sent', 'Preventivo Inviato'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Campi opzionali per collegare la notifica a oggetti specifici
    related_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='triggered_notifications'
    )
    related_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Segna la notifica come letta"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])