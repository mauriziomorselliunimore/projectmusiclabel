from django.db import connection
from django.db.utils import ProgrammingError, OperationalError

def messaging_context(request):
    """Context processor sicuro per messaggi e notifiche"""
    context = {
        'unread_messages_count': 0,
        'unread_notifications_count': 0
    }
    
    if not request.user.is_authenticated:
        return context
    
    try:
        # Verifica che le tabelle esistano prima di importare i modelli
        with connection.cursor() as cursor:
            # Check PostgreSQL per tabelle messaging
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'messaging_conversation'
                );
            """)
            conversation_exists = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'messaging_message'
                );
            """)
            message_exists = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'messaging_notification'
                );
            """)
            notification_exists = cursor.fetchone()[0]
        
        # Solo se tutte le tabelle esistono
        if conversation_exists and message_exists and notification_exists:
            from .models import Message, Notification
            
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
        
    except (ProgrammingError, OperationalError, ImportError, AttributeError) as e:
        # Durante il build o se le tabelle non esistono, ritorna zero
        pass
    
    return context