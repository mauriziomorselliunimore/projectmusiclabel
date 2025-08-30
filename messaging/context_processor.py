from .models import Message, Notification


def messaging_context(request):
    """Context processor per conteggi messaggi e notifiche"""
    context = {
        'unread_messages_count': 0,
        'unread_notifications_count': 0
    }
    
    if request.user.is_authenticated:
        # Conta messaggi non letti
        context['unread_messages_count'] = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        
        # Conta notifiche non lette
        context['unread_notifications_count'] = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
    
    return context