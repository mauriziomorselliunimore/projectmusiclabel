from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import json

from messaging.models import Message, Conversation

@login_required
@require_POST
def quick_message(request):
    """Vista per inviare un messaggio rapido a un artista"""
    try:
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        message_type = data.get('message_type', 'general')
        subject = data.get('subject', '').strip()
        message_text = data.get('message', '').strip()
        
        if not all([recipient_id, subject, message_text]):
            return JsonResponse({
                'success': False,
                'error': 'Tutti i campi sono obbligatori'
            })
            
        # Get recipient user
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Destinatario non trovato'
            })
            
        # Get or create conversation
        conversation = Conversation.objects.filter(
            participant_1__in=[request.user, recipient],
            participant_2__in=[request.user, recipient]
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create(
                participant_1=request.user,
                participant_2=recipient
            )
        
        # Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            subject=subject,
            content=message_text,
            message_type=message_type
        )
        
        # Update conversation
        conversation.update_last_message(message)
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
