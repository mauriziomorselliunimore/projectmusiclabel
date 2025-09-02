from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
import json

from .models import Conversation, Message, Notification
from .forms import MessageForm

@login_required
def get_new_messages(request, conversation_id):
    """API endpoint per il polling dei nuovi messaggi"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    last_message_id = request.GET.get('last_message_id', '0')
    
    # Verifica che l'utente sia parte della conversazione
    if request.user not in [conversation.participant_1, conversation.participant_2]:
        return JsonResponse({'error': 'Non autorizzato'}, status=403)
    
    # Recupera i nuovi messaggi
    new_messages = Message.objects.filter(
        conversation=conversation,
        id__gt=last_message_id
    ).order_by('created_at')
    
    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'subject': msg.subject,
            'is_sender': msg.sender == request.user,
            'sender_name': msg.sender.get_full_name(),
            'sender_avatar': msg.sender.profile.get_avatar_url(),
            'timestamp': msg.created_at.strftime('%H:%M')
        })
    
    return JsonResponse({'messages': messages_data})


@login_required
@require_POST
def api_send_message(request):
    """API endpoint per l'invio di messaggi rapidi"""
    try:
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        content = data.get('content')

        if not recipient_id or not content:
            return JsonResponse({
                'success': False,
                'error': 'Dati mancanti'
            }, status=400)

        recipient = get_object_or_404(User, id=recipient_id)

        # Trova o crea la conversazione
        conversation = Conversation.objects.filter(
            (Q(participant_1=request.user, participant_2=recipient) |
             Q(participant_1=recipient, participant_2=request.user))
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(
                participant_1=request.user,
                participant_2=recipient
            )

        # Crea il messaggio
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        # Crea notifica per il destinatario
        Notification.objects.create(
            recipient=recipient,
            sender=request.user,
            notification_type='message',
            content=f'Nuovo messaggio da {request.user.get_full_name() or request.user.username}',
            related_object=message
        )

        return JsonResponse({
            'success': True,
            'conversation_url': reverse('messaging:conversation', args=[conversation.id])
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def inbox(request):
    """Vista per la lista delle conversazioni (inbox)"""
    conversations = Conversation.objects.filter(
        Q(participant_1=request.user) | Q(participant_2=request.user)
    ).select_related('participant_1', 'participant_2', 'last_message')
    
    # Aggiungi info extra per ogni conversazione
    conversation_data = []
    for conv in conversations:
        other_user = conv.get_other_participant(request.user)
        if other_user:  # Solo se l'altro utente esiste
            unread_count = conv.unread_count_for_user(request.user)
            last_message = conv.messages.order_by('-created_at').first() if not conv.last_message else conv.last_message
            
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
        id=conversation_id
    )
    
    # Verifica che l'utente sia partecipante della conversazione
    if request.user not in [conversation.participant_1, conversation.participant_2]:
        messages.error(request, 'Non hai accesso a questa conversazione!')
        return redirect('messaging:inbox')
    
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
            message.recipient = conversation.get_other_participant(request.user)
            message.save()
            
            # Crea notifica per l'altro utente
            create_message_notification(
                user=message.recipient,
                sender=request.user,
                conversation=conversation
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'id': message.id,
                        'content': message.message,
                        'sender_name': message.sender.get_full_name() or message.sender.username,
                        'sent_at': message.created_at.strftime('%H:%M'),
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
        Q(participant_1=request.user, participant_2=recipient) |
        Q(participant_1=recipient, participant_2=request.user)
    ).first()
    
    # Se non esiste, creala
    if not conversation:
        conversation = Conversation.get_or_create_conversation(request.user, recipient)
    
    # Se è una richiesta POST, invia il messaggio direttamente
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.recipient = recipient
            message.save()
            
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
        Q(conversation__participant_1=request.user) | Q(conversation__participant_2=request.user),
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
        notification_type='new_message',
        title='Nuovo messaggio',
        message=f'{sender.get_full_name() or sender.username} ti ha inviato un messaggio',
        related_user=sender,
        action_url=f'/messaging/conversation/{conversation.id}/'
    )