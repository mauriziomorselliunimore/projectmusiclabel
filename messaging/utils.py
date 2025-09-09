from .models import Notification, Conversation, Message


def create_notification(user, notification_type, title, message, related_user=None, related_url=None):
    """Utility per creare notifiche"""
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_user=related_user,
        related_url=related_url
    )


def get_or_create_conversation(user1, user2):
    """Ottiene o crea una conversazione tra due utenti"""
    conversation = Conversation.objects.filter(
        participants=user1
    ).filter(
        participants=user2
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.set([user1, user2])
    
    return conversation


def send_message(sender, recipient, content):
    """Utility per inviare un messaggio"""
    conversation = get_or_create_conversation(sender, recipient)
    
    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        content=content
    )
    
    # Aggiorna timestamp conversazione
    from django.utils import timezone
    conversation.updated_at = timezone.now()
    conversation.save()
    
    # Crea notifica per il destinatario
    create_notification(
        user=recipient,
        notification_type='message',
        title='Nuovo messaggio',
        message=f'{sender.get_full_name() or sender.username} ti ha inviato un messaggio',
        related_user=sender,
        related_url=f'/messaging/conversation/{conversation.id}/'
    )
    
    return message


def get_unread_counts(user):
    """Ottiene conteggi messaggi e notifiche non letti per un utente"""
    if not user.is_authenticated:
        return {'messages': 0, 'notifications': 0}
    
    unread_messages = Message.objects.filter(
        conversation__participants=user,
        is_read=False
    ).exclude(sender=user).count()
    
    unread_notifications = Notification.objects.filter(
        user=user,
        is_read=False
    ).count()
    
    return {
        'messages': unread_messages,
        'notifications': unread_notifications
    }


def mark_conversation_as_read(conversation, user):
    """Segna tutti i messaggi di una conversazione come letti per un utente"""
    unread_messages = conversation.messages.filter(
        is_read=False
    ).exclude(sender=user)
    
    for message in unread_messages:
        message.mark_as_read()


# Utility per creare notifiche specifiche del sistema

def notify_booking_request(associate_user, artist_user, booking):
    """Notifica nuova richiesta di prenotazione"""
    create_notification(
        user=associate_user,
        notification_type='booking',
        title='Nuova richiesta di prenotazione',
        message=f'{artist_user.get_full_name() or artist_user.username} ha richiesto una prenotazione',
        related_user=artist_user,
        related_url=f'/booking/manage/{booking.id}/'  # URL da adattare
    )


def notify_booking_confirmed(artist_user, associate_user, booking):
    """Notifica prenotazione confermata"""
    create_notification(
        user=artist_user,
        notification_type='booking_confirmed',
        title='Prenotazione confermata',
        message=f'{associate_user.get_full_name() or associate_user.username} ha confermato la tua prenotazione',
        related_user=associate_user,
        related_url=f'/booking/detail/{booking.id}/'  # URL da adattare
    )


def notify_booking_cancelled(recipient_user, sender_user, booking):
    """Notifica prenotazione cancellata"""
    create_notification(
        user=recipient_user,
        notification_type='booking_cancelled',
        title='Prenotazione cancellata',
        message=f'{sender_user.get_full_name() or sender_user.username} ha cancellato una prenotazione',
        related_user=sender_user,
        related_url=f'/booking/detail/{booking.id}/'  # URL da adattare
    )


def notify_demo_feedback(artist_user, feedback_user, demo):
    """Notifica feedback su demo"""
    create_notification(
        user=artist_user,
        notification_type='demo_feedback',
        title='Nuovo feedback su demo',
        message=f'{feedback_user.get_full_name() or feedback_user.username} ha lasciato un feedback sulla tua demo',
        related_user=feedback_user,
        related_url=f'/artists/demo/{demo.id}/'  # URL da adattare
    )


def notify_profile_view(profile_owner, viewer):
    """Notifica visualizzazione profilo (opzionale - potrebbe essere troppo invasivo)"""
    # Evita di notificare se la persona visualizza il proprio profilo
    if profile_owner != viewer:
        create_notification(
            user=profile_owner,
            notification_type='profile_view',
            title='Profilo visualizzato',
            message=f'{viewer.get_full_name() or viewer.username} ha visualizzato il tuo profilo',
            related_user=viewer,
            related_url=f'/accounts/profile/'  # URL da adattare
        )


def cleanup_old_notifications(days=30):
    """Utility per pulire notifiche vecchie (da usare con cron job)"""
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    # Elimina notifiche lette più vecchie di X giorni
    deleted_count = Notification.objects.filter(
        is_read=True,
        created_at__lt=cutoff_date
    ).delete()
    
    return deleted_count[0] if deleted_count else 0