from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth.models import User

from ..models import Artist, Demo
from ..forms import ArtistForm, DemoForm
from . import messages as app_messages  # Rename import to avoid conflict

def artist_list(request):
    """List all active artists"""
    artists = Artist.objects.filter(is_active=True)
    return render(request, 'artists/artist_list.html', {'artists': artists})

def artist_detail(request, pk):
    """Show artist details"""
    artist = get_object_or_404(Artist, pk=pk)
    demos = Demo.objects.filter(artist=artist, is_public=True)
    return render(request, 'artists/artist_detail.html', {
        'artist': artist,
        'demos': demos
    })

@login_required
def artist_create(request):
    """Create new artist profile"""
    if hasattr(request.user, 'artist'):
        django_messages.warning(request, 'Hai già un profilo artista!')
        return redirect('artists:profile')
        
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
            artist.save()
            django_messages.success(request, 'Profilo artista creato con successo!')
            return redirect('artists:profile')
    else:
        form = ArtistForm()
        
    return render(request, 'artists/artist_form.html', {'form': form})

@login_required
def artist_profile(request):
    """Display artist profile"""
    if not hasattr(request.user, 'artist'):
        django_messages.warning(request, 'Non hai ancora un profilo artista!')
        return redirect('artists:create')
    
    artist = request.user.artist
    demos = Demo.objects.filter(artist=artist)
    return render(request, 'artists/artist_profile.html', {
        'artist': artist,
        'demos': demos
    })

@login_required
def artist_edit(request, pk):
    """Edit artist profile"""
    artist = get_object_or_404(Artist, pk=pk, user=request.user)
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            # Salva i dati dell'artista
            artist = form.save()
            
            # Aggiorna i campi del profilo
            profile.external_avatar_url = form.cleaned_data.get('external_avatar_url', '')
            profile.profile_icon = form.cleaned_data.get('profile_icon', profile.profile_icon)
            profile.profile_icon_color = form.cleaned_data.get('profile_icon_color', profile.profile_icon_color)
            profile.save()
            
            django_messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('artists:profile')
    else:
        # Popola il form con i dati esistenti
        initial_data = {
            'external_avatar_url': profile.external_avatar_url,
            'profile_icon': profile.profile_icon,
            'profile_icon_color': profile.profile_icon_color,
        }
        form = ArtistForm(instance=artist, initial=initial_data)
        
    return render(request, 'artists/artist_form.html', {'form': form, 'artist': artist})

@login_required
def demo_upload(request):
    """Upload a new demo"""
    if request.method == 'POST':
        form = DemoForm(request.POST, request.FILES)
        if form.is_valid():
            demo = form.save(commit=False)
            demo.artist = request.user.artist
            demo.save()
            django_messages.success(request, 'Demo caricato con successo!')
            return redirect('artists:profile')
    else:
        form = DemoForm()
    
    return render(request, 'artists/demo_form.html', {'form': form})

@login_required
def demo_delete(request, pk):
    """Delete a demo"""
    demo = get_object_or_404(Demo, pk=pk, artist=request.user.artist)
    demo.delete()
    django_messages.success(request, 'Demo eliminato con successo!')
    return redirect('artists:profile')

@login_required
def quick_message(request):
    """Send a quick message to an artist"""
    if request.method != 'POST':
        return redirect('artists:list')
        
    artist_id = request.POST.get('artist')
    message = request.POST.get('message')
    
    if not message or not artist_id:
        django_messages.error(request, 'Devi inserire un messaggio!')
        return redirect('artists:list')
        
    try:
        recipient = Artist.objects.get(pk=artist_id)
        # Use messaging system to send the message
        from messaging.models import Message
        Message.objects.create(
            sender=request.user,
            recipient=recipient.user,
            content=message
        )
        django_messages.success(request, 'Messaggio inviato!')
    except Artist.DoesNotExist:
        django_messages.error(request, 'Artista non trovato!')
    
    return redirect('artists:list')
    
    return render(request, 'artists/demo_form.html', {'form': form, 'demo': demo})

@login_required
def demo_delete(request, pk):
    """View for deleting a demo"""
    demo = get_object_or_404(Demo, pk=pk, artist=request.user.artist)
    demo.delete()
    django_messages.success(request, 'Demo eliminato con successo!')
    return redirect('artists:profile')
