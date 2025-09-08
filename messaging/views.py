"""
Views per la gestione dei messaggi
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Conversation, Message, Notification
from .forms import MessageForm


def mark_messages_as_read(conversation, user):
    """Segna i messaggi di una conversazione come letti"""
    Message.objects.filter(
        conversation=conversation,
        recipient=user,
        is_read=False
    ).update(is_read=True)


def clear_notifications(conversation, user):
    """Rimuove le notifiche per una conversazione"""
    Notification.objects.filter(
        user=user,
        notification_type='new_message',
        related_message__conversation=conversation
    ).delete()


@login_required
def get_new_messages(request, conversation_id):
    """
    Vista API per ottenere i nuovi messaggi in una conversazione
    Usata per il polling AJAX
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Verifica che l'utente sia partecipante alla conversazione
    if request.user not in [conversation.participant_1, conversation.participant_2]:
        return JsonResponse({'error': 'Non autorizzato'}, status=403)
    
    # Ottieni i messaggi non letti per questo utente
    new_messages = Message.objects.filter(
        conversation=conversation,
        recipient=request.user,
        is_read=False
    ).order_by('created_at')
    
    # Formatta i messaggi per JSON
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'is_read': msg.is_read
    } for msg in new_messages]
    
    # Segna i messaggi come letti
    new_messages.update(is_read=True)
    
    # Rimuovi le notifiche associate
    clear_notifications(conversation, request.user)
    
    return JsonResponse({
        'messages': messages_data
    })


def create_message_notification(message):
    """Crea una notifica per un nuovo messaggio"""
    Notification.objects.create(
        user=message.recipient,
        notification_type='new_message',
        title=f'Nuovo messaggio da {message.sender.get_full_name()}',
        message=message.message[:100],
        related_message=message,
        related_user=message.sender
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
            
            create_message_notification(msg)
            
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


@login_required
def inbox(request):
    """Vista per la inbox dei messaggi"""
    conversations = Conversation.objects.filter(
        Q(participant_1=request.user) | Q(participant_2=request.user)
    ).order_by('-last_message_date')
    
    context = {
        'conversations': conversations
    }
    
    return render(request, 'messaging/inbox.html', context)


@login_required
def start_conversation(request, user_id):
    """Avvia una nuova conversazione con un utente"""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, 'Non puoi avviare una conversazione con te stesso!')
        return redirect('messaging:inbox')
    
    # Cerca una conversazione esistente o ne crea una nuova
    conversation = Conversation.get_or_create_conversation(request.user, other_user)
    
    return redirect('messaging:conversation', conversation_id=conversation.id)


@login_required
def send_message(request, user_id):
    """Vista per inviare un nuovo messaggio a un utente"""
    recipient = get_object_or_404(User, id=user_id)
    
    if recipient == request.user:
        messages.error(request, 'Non puoi inviare messaggi a te stesso!')
        return redirect('messaging:inbox')
    
    conversation = Conversation.get_or_create_conversation(request.user, recipient)
    return redirect('messaging:conversation', conversation_id=conversation.id)


@login_required
def notifications(request):
    """Vista per mostrare tutte le notifiche"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'messaging/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    """Segna una notifica come letta"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('messaging:notifications')


@login_required
def mark_all_notifications_read(request):
    """Segna tutte le notifiche come lette"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('messaging:notifications')


@login_required
def get_unread_counts(request):
    """API per ottenere il numero di messaggi e notifiche non letti"""
    unread_messages = Message.objects.filter(
        conversation__in=Conversation.objects.filter(
            Q(participant_1=request.user) | Q(participant_2=request.user)
        ),
        recipient=request.user,
        is_read=False
    ).count()
    
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications
    })


@login_required
def api_send_message(request):
    """API per inviare messaggi via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo non consentito'}, status=405)
    
    recipient_id = request.POST.get('recipient_id')
    message_text = request.POST.get('message')
    
    if not recipient_id or not message_text:
        return JsonResponse({'success': False, 'error': 'Dati mancanti'}, status=400)
    
    try:
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.get_or_create_conversation(request.user, recipient)
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            message=message_text
        )
        
        create_message_notification(message)
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.message,
                'sender_name': message.sender.get_full_name(),
                'timestamp': message.created_at.strftime('%H:%M')
            }
        })
        
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utente non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)