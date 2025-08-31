from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


class Conversation(models.Model):
    """Rappresenta una conversazione tra due utenti"""
    participant_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_participant_1')
    participant_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_participant_2')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    last_message_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = [['participant_1', 'participant_2']]
    
    def __str__(self):
        return f"Conversazione: {self.participant_1.get_full_name()} - {self.participant_2.get_full_name()}"
    
    def get_other_participant(self, user):
        """Ottiene l'altro partecipante della conversazione"""
        if user == self.participant_1:
            return self.participant_2
        elif user == self.participant_2:
            return self.participant_1
        return None
    
    def update_last_message(self, message):
        """Aggiorna l'ultimo messaggio della conversazione"""
        self.last_message = message
        self.last_message_date = message.created_at
        self.updated_at = timezone.now()
        self.save(update_fields=['last_message', 'last_message_date', 'updated_at'])
    
    def has_unread_messages(self, user):
        """Controlla se ci sono messaggi non letti per l'utente"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).exists()
    
    def unread_count_for_user(self, user):
        """Conta i messaggi non letti per l'utente specificato"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).count()
    
    def get_absolute_url(self):
        return reverse('messaging:conversation', kwargs={'conversation_id': self.pk})
    
    @classmethod
    def get_or_create_conversation(cls, user1, user2):
        """Ottiene o crea una conversazione tra due utenti"""
        # Assicurati che user1 abbia sempre ID minore per consistenza
        if user1.id > user2.id:
            user1, user2 = user2, user1
        
        conversation = cls.objects.filter(
            Q(participant_1=user1, participant_2=user2) |
            Q(participant_1=user2, participant_2=user1)
        ).first()
        
        if not conversation:
            conversation = cls.objects.create(
                participant_1=user1,
                participant_2=user2
            )
        
        return conversation


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
        Conversation, 
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
    message = models.TextField()
    
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


class Notification(models.Model):
    """Sistema di notifiche generico"""
    NOTIFICATION_TYPES = [
        ('new_message', 'Nuovo Messaggio'),
        ('booking_request', 'Richiesta Prenotazione'),
        ('booking_confirmed', 'Prenotazione Confermata'),
        ('booking_cancelled', 'Prenotazione Cancellata'),
        ('demo_feedback', 'Feedback Demo'),
        ('profile_view', 'Profilo Visualizzato'),
        ('quote_request', 'Richiesta Preventivo'),
        ('quote_sent', 'Preventivo Inviato'),
        ('system', 'Notifica di Sistema'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.CharField(max_length=500, blank=True)
    
    # Stati
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Collegamenti opzionali
    related_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='triggered_notifications'
    )
    related_message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    related_booking = models.ForeignKey(
        'booking.Booking',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Segna la notifica come letta"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    @property
    def is_recent(self):
        """Controlla se la notifica è stata creata nelle ultime 24 ore"""
        return (timezone.now() - self.created_at).total_seconds() < 86400
    
    @property
    def icon_class(self):
        """Restituisce la classe CSS per l'icona della notifica"""
        icons = {
            'new_message': 'bi-chat-fill',
            'booking_request': 'bi-calendar-plus',
            'booking_confirmed': 'bi-check-circle-fill',
            'booking_cancelled': 'bi-x-circle-fill',
            'demo_feedback': 'bi-music-note-beamed',
            'profile_view': 'bi-eye-fill',
            'quote_request': 'bi-calculator',
            'quote_sent': 'bi-envelope-check',
            'system': 'bi-gear-fill',
        }
        return icons.get(self.notification_type, 'bi-bell-fill')
    
    @property
    def color_class(self):
        """Restituisce la classe CSS per il colore della notifica"""
        colors = {
            'new_message': 'text-primary',
            'booking_request': 'text-warning',
            'booking_confirmed': 'text-success',
            'booking_cancelled': 'text-danger',
            'demo_feedback': 'text-info',
            'profile_view': 'text-secondary',
            'quote_request': 'text-warning',
            'quote_sent': 'text-success',
            'system': 'text-muted',
        }
        return colors.get(self.notification_type, 'text-primary')