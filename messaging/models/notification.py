from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
        'messaging.Message',
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
