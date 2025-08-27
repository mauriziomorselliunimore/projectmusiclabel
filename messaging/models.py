from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Message(models.Model):
    """Sistema messaggistica interna tra utenti"""
    MESSAGE_TYPES = [
        ('general', 'Messaggio Generale'),
        ('booking_request', 'Richiesta Prenotazione'),
        ('booking_update', 'Aggiornamento Prenotazione'),
        ('collaboration', 'Proposta Collaborazione'),
        ('inquiry', 'Richiesta Info'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    # Contenuto messaggio
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=2000)
    
    # Collegamenti opzionali
    related_booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.subject}"
    
    def get_absolute_url(self):
        return reverse('messaging:detail', kwargs={'pk': self.pk})
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    @property
    def is_recent(self):
        """Messaggio degli ultimi 3 giorni"""
        return (timezone.now() - self.created_at).days <= 3


class Notification(models.Model):
    """Sistema notifiche per email/in-app"""
    NOTIFICATION_TYPES = [
        ('booking_request', 'Richiesta Prenotazione'),
        ('booking_confirmed', 'Prenotazione Confermata'),
        ('booking_cancelled', 'Prenotazione Cancellata'),
        ('new_message', 'Nuovo Messaggio'),
        ('demo_uploaded', 'Nuova Demo'),
        ('profile_view', 'Visualizzazione Profilo'),
        ('system', 'Notifica Sistema'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    
    # Contenuto
    title = models.CharField(max_length=200)
    message = models.TextField(max_length=500)
    action_url = models.URLField(blank=True, help_text="Link azione (opzionale)")
    
    # Collegamenti per context
    related_booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, null=True, blank=True)
    related_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                                   related_name='notifications_about')
    
    # Status
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}: {self.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    @property
    def is_recent(self):
        """Notifica degli ultimi 7 giorni"""
        return (timezone.now() - self.created_at).days <= 7
    
    @property
    def icon_class(self):
        """Icona Bootstrap per tipo notifica"""
        icons = {
            'booking_request': 'bi-calendar-plus',
            'booking_confirmed': 'bi-calendar-check',
            'booking_cancelled': 'bi-calendar-x',
            'new_message': 'bi-envelope',
            'demo_uploaded': 'bi-music-note-beamed',
            'profile_view': 'bi-person',
            'system': 'bi-gear',
        }
        return icons.get(self.notification_type, 'bi-info-circle')
    
    @property
    def color_class(self):
        """Classe colore per tipo notifica"""
        colors = {
            'booking_request': 'text-warning',
            'booking_confirmed': 'text-success',
            'booking_cancelled': 'text-danger',
            'new_message': 'text-primary',
            'demo_uploaded': 'text-info',
            'profile_view': 'text-secondary',
            'system': 'text-muted',
        }
        return colors.get(self.notification_type, 'text-muted')


class Conversation(models.Model):
    """Thread di conversazione tra due utenti"""
    participant_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_p1')
    participant_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_p2')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.Dat