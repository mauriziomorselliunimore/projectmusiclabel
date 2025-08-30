from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .models import Conversation, Message, Notification
from .forms import MessageForm


@login_required
def inbox(request):
    """Vista per la lista delle conversazioni (inbox)"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages')
    
    # Aggiungi info extra per ogni conversazione
    conversation_data = []
    for conv in conversations:
        other_user = conv.get_other_participant(request.user)
        last_message = conv.get_last_message()
        unread_count = conv.unread_count(request.user)
        
        conversation_data.append({
            'conversation': conv,
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count,
            'has_unread': unread_count > 0
        })
    
    context = {
        'conversations': conversation_data,
        'total_unread': sum(c['unread_count'] for c in conversation_data)
    }
    
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Vista per una singola conversazione"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )
    
    # Segna tutti i messaggi come letti
    unread_messages = conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user)
    
    for message in unread_messages:
        message.mark_as_read()
    
    # Ottieni tutti i messaggi della conversazione
    messages_list = conversation.messages.all().select_related('sender')
    
    # Gestisci invio nuovo messaggio
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Aggiorna timestamp conversazione
            conversation.updated_at = timezone.now()
            conversation.save()
            
            # Crea notifica per l'altro utente
            other_user = conversation.get_other_participant(request.user)
            create_message_notification(
                user=other_user,
                sender=request.user,
                conversation=conversation
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'id': message.id,
                        'content': message.content,
                        'sender_name': message.sender.get_full_name() or message.sender.username,
                        'sent_at': message.sent_at.strftime('%H:%M'),
                        'is_own': True
                    }
                })
            
            return redirect('messaging:conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    other_user = conversation.get_other_participant(request.user)
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
        'other_user': other_user
    }
    
    return render(request, 'messaging/conversation.html', context)


@login_required
def send_message(request, user_id):
    """Inizia una nuova conversazione o reindirizza a quella esistente"""
    recipient = get_object_or_404(User, id=user_id)
    
    if recipient == request.user:
        messages.error(request, "Non puoi inviare messaggi a te stesso!")
        return redirect('core:home')
    
    # Cerca conversazione esistente
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=recipient
    ).first()
    
    # Se non esiste, creala
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.set([request.user, recipient])
    
    # Se è una richiesta POST, invia il messaggio direttamente
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            conversation.updated_at = timezone.now()
            conversation.save()
            
            # Crea notifica
            create_message_notification(
                user=recipient,
                sender=request.user,
                conversation=conversation
            )
            
            messages.success(request, f"Messaggio inviato a {recipient.get_full_name() or recipient.username}!")
            return redirect('messaging:conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    context = {
        'recipient': recipient,
        'form': form,
        'conversation': conversation
    }
    
    return render(request, 'messaging/send_message.html', context)


@login_required
def notifications(request):
    """Vista per le notifiche dell'utente"""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).select_related('related_user')
    
    # Separa lette e non lette
    unread_notifications = user_notifications.filter(is_read=False)
    read_notifications = user_notifications.filter(is_read=True)[:20]  # Ultime 20
    
    context = {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'unread_count': unread_notifications.count()
    }
    
    return render(request, 'messaging/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Segna una notifica come letta"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )
    
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('messaging:notifications')


@login_required
@require_POST
def mark_all_notifications_read(request):
    """Segna tutte le notifiche come lette"""
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('messaging:notifications')


# API per aggiornamenti real-time (opzionale)
@login_required
def get_unread_counts(request):
    """API per ottenere conteggi messaggi/notifiche non letti"""
    # Conta messaggi non letti
    unread_messages = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    # Conta notifiche non lette
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications
    })


def create_message_notification(user, sender, conversation):
    """Utility per creare notifica nuovo messaggio"""
    Notification.objects.create(
        user=user,
        notification_type='message',
        title='Nuovo messaggio',
        message=f'{sender.get_full_name() or sender.username} ti ha inviato un messaggio',
        related_user=sender,
        related_url=f'/messaging/conversation/{conversation.id}/'
    )