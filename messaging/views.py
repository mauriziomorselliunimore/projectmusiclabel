from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.core.paginator import Paginator
import json

from .models import Message, Notification, Conversation
from .forms import MessageForm

@login_required
def inbox(request):
    """Dashboard principale messaggi"""
    # Statistiche rapide
    unread_messages = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    # Messaggi recenti
    recent_messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender', 'sender__profile').order_by('-created_at')[:5]
    
    # Notifiche recenti
    recent_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Conversazioni attive
    conversations = Conversation.objects.filter(
        Q(participant_1=request.user) | Q(participant_2=request.user)
    ).select_related('participant_1', 'participant_2', 'last_message').order_by('-updated_at')[:5]
    
    context = {
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications,
        'recent_messages': recent_messages,
        'recent_notifications': recent_notifications,
        'conversations': conversations,
    }
    
    return render(request, 'messaging/inbox.html', context)

@login_required
def conversations_list(request):
    """Lista tutte le conversazioni"""
    conversations = Conversation.objects.filter(
        Q(participant_1=request.user) | Q(participant_2=request.user)
    ).select_related('participant_1', 'participant_2', 'last_message').order_by('-updated_at')
    
    paginator = Paginator(conversations, 15)
    page_number = request.GET.get('page')
    conversations = paginator.get_page(page_number)
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'messaging/conversations_list.html', context)

@login_required
def conversation_detail(request, pk):
    """Dettaglio conversazione con tutti i messaggi"""
    conversation = get_object_or_404(Conversation, pk=pk)
    
    # Verifica che l'utente faccia parte della conversazione
    if request.user not in [conversation.participant_1, conversation.participant_2]:
        messages.error(request, 'Non hai accesso a questa conversazione!')
        return redirect('messaging:inbox')
    
    # Ottieni tutti i messaggi
    conversation_messages = conversation.get_messages().select_related('sender')
    
    # Segna come letti i messaggi destinati all'utente corrente
    conversation_messages.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    # Altro partecipante
    other_participant = conversation.get_other_participant(request.user)
    
    # Form per nuovo messaggio
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_participant
            message.save()
            
            # Aggiorna conversazione
            conversation.update_last_message(message)
            
            messages.success(request, 'Messaggio inviato!')
            return redirect('messaging:conversation', pk=pk)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conversation,
        'messages': conversation_messages,
        'other_participant': other_participant,
        'form': form,
    }
    
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def send_message(request, recipient_id):
    """Invia nuovo messaggio"""
    recipient = get_object_or_404(User, id=recipient_id)
    
    if request.user == recipient:
        messages.error(request, 'Non puoi inviare un messaggio a te stesso!')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            
            # Crea o aggiorna conversazione
            conversation = Conversation.get_or_create_conversation(request.user, recipient)
            conversation.update_last_message(message)
            
            # Crea notifica per destinatario
            Notification.objects.create(
                user=recipient,
                notification_type='new_message',
                title=f'Nuovo messaggio da {request.user.get_full_name()}',
                message=f'Oggetto: {message.subject}',
                action_url=message.get_absolute_url(),
                related_message=message,
                related_user=request.user
            )
            
            messages.success(request, f'Messaggio inviato a {recipient.get_full_name()}!')
            return redirect('messaging:conversation', pk=conversation.pk)
    else:
        # Pre-riempi il form se ci sono parametri GET
        initial_data = {}
        if request.GET.get('subject'):
            initial_data['subject'] = request.GET.get('subject')
        if request.GET.get('message'):
            initial_data['message'] = request.GET.get('message')
        
        form = MessageForm(initial=initial_data)
    
    context = {
        'form': form,
        'recipient': recipient,
    }
    
    return render(request, 'messaging/send_message.html', context)

@login_required
def message_detail(request, pk):
    """Dettaglio singolo messaggio"""
    message = get_object_or_404(Message, pk=pk)
    
    # Verifica permessi
    if request.user not in [message.sender, message.recipient]:
        messages.error(request, 'Non hai accesso a questo messaggio!')
        return redirect('messaging:inbox')
    
    # Segna come letto se è il destinatario
    if request.user == message.recipient:
        message.mark_as_read()
    
    context = {
        'message': message,
    }
    
    return render(request, 'messaging/message_detail.html', context)

@login_required
def reply_message(request, pk):
    """Rispondi a un messaggio"""
    original_message = get_object_or_404(Message, pk=pk)
    
    # Verifica permessi
    if request.user not in [original_message.sender, original_message.recipient]:
        messages.error(request, 'Non hai accesso a questo messaggio!')
        return redirect('messaging:inbox')
    
    # Determina il destinatario della risposta
    recipient = original_message.sender if request.user == original_message.recipient else original_message.recipient
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = recipient
            reply.message_type = original_message.message_type
            reply.related_booking = original_message.related_booking
            reply.save()
            
            messages.success(request, 'Risposta inviata!')
            
            # Trova o crea conversazione
            conversation = Conversation.get_or_create_conversation(request.user, recipient)
            return redirect('messaging:conversation', pk=conversation.pk)
    else:
        # Pre-riempi con Re: nel subject
        subject = original_message.subject
        if not subject.startswith('Re:'):
            subject = f'Re: {subject}'
        
        form = MessageForm(initial={
            'subject': subject,
            'message_type': original_message.message_type,
        })
    
    context = {
        'form': form,
        'original_message': original_message,
        'recipient': recipient,
    }
    
    return render(request, 'messaging/reply_message.html', context)

@login_required
def notifications_list(request):
    """Lista notifiche utente"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Filtro per tipo se specificato
    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    # Paginazione
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)
    
    # Segna come lette le notifiche visualizzate
    notification_ids = [n.id for n in notifications if not n.is_read]
    if notification_ids:
        Notification.objects.filter(id__in=notification_ids).update(is_read=True)
    
    context = {
        'notifications': notifications,
        'notification_type': notification_type,
        'notification_types': Notification.NOTIFICATION_TYPES,
    }
    
    return render(request, 'messaging/notifications_list.html', context)

@login_required
@require_POST
def mark_notifications_read(request):
    """Segna tutte le notifiche come lette (AJAX)"""
    try:
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({
            'success': True,
            'updated': updated,
            'message': f'{updated} notifiche segnate come lette.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# messaging/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
t        fields = ['message_type', 'subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Oggetto del messaggio'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Scrivi il tuo messaggio...'
            }),
            'message_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'message_type': 'Tipo Messaggio',
            'subject': 'Oggetto',
            'message': 'Messaggio',
        }