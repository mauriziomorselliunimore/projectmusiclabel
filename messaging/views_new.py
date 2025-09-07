"""
Views per la gestione dei messaggi
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Conversation, Message, Notification
from .forms import MessageForm


def mark_messages_as_read(conversation, user):
    """Segna i messaggi di una conversazione come letti"""
    Message.objects.filter(
        conversation=conversation,
        receiver=user,
        is_read=False
    ).update(is_read=True)


def clear_notifications(conversation, user):
    """Rimuove le notifiche per una conversazione"""
    Notification.objects.filter(
        user=user,
        notification_type='message',
        conversation=conversation
    ).delete()


def create_message_notification(message, conversation):
    """Crea una notifica per un nuovo messaggio"""
    Notification.objects.create(
        user=message.recipient,
        notification_type='new_message',
        title=f'Nuovo messaggio da {message.sender.get_full_name()}',
        message=message.message[:100],
        related_message=message,
        related_user=message.sender,
        conversation=conversation
    )


@login_required
def conversation_detail(request, conversation_id):
    """Vista dettaglio conversazione"""
    conv = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user not in [conv.participant_1, conv.participant_2]:
        messages.error(request, 'Non hai accesso a questa conversazione!')
        return redirect('messaging:inbox')
    
    mark_messages_as_read(conv, request.user)
    clear_notifications(conv, request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conv
            msg.sender = request.user
            msg.recipient = conv.get_other_participant(request.user)
            msg.save()
            
            create_message_notification(msg, conv)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': {
                        'id': msg.id,
                        'content': msg.message,
                        'sender_name': msg.sender.get_full_name(),
                        'timestamp': msg.created_at.strftime('%H:%M')
                    }
                }
                return JsonResponse(data)
            
            return redirect('messaging:conversation', conversation_id=conv.id)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conv,
        'messages': conv.messages.order_by('created_at').select_related('sender'),
        'form': form,
        'other_user': conv.get_other_participant(request.user)
    }
    
    return render(request, 'messaging/conversation.html', context)
