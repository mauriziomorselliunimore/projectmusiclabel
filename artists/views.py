from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User

from messaging.models import Message, Notification, Conversation
from .models import Artist, Demo
from .forms import ArtistForm, DemoForm


def artist_list(request):
    """Lista tutti gli artisti con ricerca"""
    query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')

    artists = Artist.objects.filter(is_active=True)

    if query:
        artists = artists.filter(
            Q(stage_name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(genres__icontains=query) |
            Q(bio__icontains=query)
        )

    if genre_filter:
        artists = artists.filter(genres__icontains=genre_filter)

    context = {
        'artists': artists,
        'search_query': query,
        'genre_filter': genre_filter,
    }
    return render(request, 'artists/artist_list.html', context)


def artist_detail(request, pk):
    """Dettaglio singolo artista con integrazione messaggistica"""
    artist = get_object_or_404(Artist.objects.select_related('user'), pk=pk, is_active=True)
    demos = artist.demos.filter(is_public=True)

    is_owner = request.user == artist.user
    can_message = request.user.is_authenticated and not is_owner and hasattr(request.user, 'profile')
    can_book = request.user.is_authenticated and hasattr(request.user, 'artist') and not is_owner

    # Get existing conversation if any - FIXED VERSION
    existing_conversation = None
    if request.user.is_authenticated and not is_owner:
        try:
            existing_conversation = Conversation.objects.filter(
                Q(participant_1=request.user, participant_2=artist.user) |
                Q(participant_1=artist.user, participant_2=request.user)
            ).first()
        except Exception:
            # Se ci sono errori con il modello Conversation, ignora
            existing_conversation = None

    context = {
        'artist': artist,
        'demos': demos,
        'is_owner': is_owner,
        'can_message': can_message,
        'can_book': can_book,
        'existing_conversation': existing_conversation,
    }
    return render(request, 'artists/artist_detail.html', context)


@login_required
def artist_create(request):
    """Crea profilo artista"""
    if hasattr(request.user, 'artist'):
        messages.info(request, 'Hai già un profilo artista!')
        return redirect('artists:detail', pk=request.user.artist.pk)

    form = ArtistForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        artist = form.save(commit=False)
        artist.user = request.user
        artist.save()
        messages.success(request, 'Profilo artista creato con successo!')
        return redirect('artists:detail', pk=artist.pk)

    return render(request, 'artists/artist_form.html', {'form': form, 'title': 'Crea Profilo Artista'})


@login_required
def artist_edit(request, pk):
    """Modifica profilo artista"""
    artist = get_object_or_404(Artist, pk=pk)

    if artist.user != request.user:
        messages.error(request, 'Non hai i permessi per modificare questo profilo!')
        return redirect('artists:detail', pk=pk)

    form = ArtistForm(request.POST or None, request.FILES or None, instance=artist)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profilo aggiornato con successo!')
        return redirect('artists:detail', pk=pk)

    return render(request, 'artists/artist_form.html', {'form': form, 'title': 'Modifica Profilo'})


@login_required
def demo_upload(request):
    """Upload demo musicale"""
    if not hasattr(request.user, 'artist'):
        messages.error(request, 'Devi avere un profilo artista per caricare demo!')
        return redirect('artists:create')

    form = DemoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        demo = form.save(commit=False)
        demo.artist = request.user.artist
        demo.save()
        messages.success(request, f'Demo "{demo.title}" caricata con successo!')
        return redirect('artists:detail', pk=request.user.artist.pk)

    return render(request, 'artists/demo_form.html', {'form': form})


@login_required
def demo_delete(request, pk):
    """Elimina demo"""
    demo = get_object_or_404(Demo, pk=pk)

    if demo.artist.user != request.user:
        messages.error(request, 'Non hai i permessi per eliminare questa demo!')
        return redirect('artists:detail', pk=demo.artist.pk)

    if request.method == 'POST':
        demo.delete()
        messages.success(request, 'Demo eliminata con successo!')
        return redirect('artists:detail', pk=demo.artist.pk)

    return render(request, 'artists/demo_confirm_delete.html', {'demo': demo})


@login_required
def quick_message(request):
    """Invia messaggio rapido via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo non consentito'})

    try:
        import json
        data = json.loads(request.body)

        recipient_id = data.get('recipient_id')
        message_text = data.get('message')
        subject = data.get('subject', 'Nuovo messaggio')
        message_type = data.get('message_type', 'general')

        if not recipient_id or not message_text:
            return JsonResponse({'success': False, 'error': 'Dati mancanti'})

        recipient = User.objects.get(id=recipient_id)

        if request.user == recipient:
            return JsonResponse({'success': False, 'error': 'Non puoi inviare messaggi a te stesso'})

        # Get or create conversation
        conversation = Conversation.get_or_create_conversation(request.user, recipient)

        # Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            subject=subject,
            message=message_text,
            message_type=message_type
        )

        # Create notification
        Notification.objects.create(
            user=recipient,
            notification_type='new_message',
            title=f'Nuovo messaggio da {request.user.get_full_name()}',
            message=f'Oggetto: {subject}',
            action_url=message.get_absolute_url(),
            related_message=message,
            related_user=request.user
        )

        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'conversation_url': conversation.get_absolute_url()
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})