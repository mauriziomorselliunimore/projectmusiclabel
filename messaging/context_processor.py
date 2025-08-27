def notifications_count(request):
    """Context processor per contare notifiche non lette"""
    if request.user.is_authenticated:
        from .models import Notification, Message
        
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        unread_messages = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        return {
            'unread_notifications_count': unread_notifications,
            'unread_messages_count': unread_messages,
            'total_unread': unread_notifications + unread_messages,
        }
    
    return {
        'unread_notifications_count': 0,
        'unread_messages_count': 0,
        'total_unread': 0,
    }