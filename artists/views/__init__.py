from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from ..models import Artist, Demo
from ..forms import ArtistForm, DemoForm

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
        messages.warning(request, 'Hai già un profilo artista!')
        return redirect('artists:profile')
        
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
            artist.save()
            messages.success(request, 'Profilo artista creato con successo!')
            return redirect('artists:profile')
    else:
        form = ArtistForm()
        
    return render(request, 'artists/artist_form.html', {'form': form})

@login_required
def artist_edit(request, pk):
    """Edit artist profile"""
    artist = get_object_or_404(Artist, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('artists:profile')
    else:
        form = ArtistForm(instance=artist)
        
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
            messages.success(request, 'Demo caricato con successo!')
            return redirect('artists:profile')
    else:
        form = DemoForm()
    
    return render(request, 'artists/demo_form.html', {'form': form})

@login_required
def demo_delete(request, pk):
    """Delete a demo"""
    demo = get_object_or_404(Demo, pk=pk, artist=request.user.artist)
    demo.delete()
    messages.success(request, 'Demo eliminato con successo!')
    return redirect('artists:profile')

@login_required
def quick_message(request):
    """Send a quick message to an artist"""
    if request.method != 'POST':
        return redirect('artists:list')
        
    artist_id = request.POST.get('artist')
    message = request.POST.get('message')
    
    if not message or not artist_id:
        messages.error(request, 'Devi inserire un messaggio!')
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
        messages.success(request, 'Messaggio inviato!')
    except Artist.DoesNotExist:
        messages.error(request, 'Artista non trovato!')
    
    return redirect('artists:list')
            artist.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('artists:profile')
    else:
        form = ArtistForm(instance=artist)
    
    context = {
        'artist': artist,
        'form': form
    }
    return render(request, 'artists/profile.html', context)

@login_required
def demo_create(request):
    """View for creating a new demo"""
    if request.method == 'POST':
        form = DemoForm(request.POST, request.FILES)
        if form.is_valid():
            demo = form.save(commit=False)
            demo.artist = request.user.artist
            demo.save()
            messages.success(request, 'Demo caricato con successo!')
            return redirect('artists:profile')
    else:
        form = DemoForm()
    
    return render(request, 'artists/demo_form.html', {'form': form})

@login_required
def demo_edit(request, pk):
    """View for editing an existing demo"""
    demo = get_object_or_404(Demo, pk=pk, artist=request.user.artist)
    
    if request.method == 'POST':
        form = DemoForm(request.POST, request.FILES, instance=demo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demo aggiornato con successo!')
            return redirect('artists:profile')
    else:
        form = DemoForm(instance=demo)
    
    return render(request, 'artists/demo_form.html', {'form': form, 'demo': demo})

@login_required
def demo_delete(request, pk):
    """View for deleting a demo"""
    demo = get_object_or_404(Demo, pk=pk, artist=request.user.artist)
    demo.delete()
    messages.success(request, 'Demo eliminato con successo!')
    return redirect('artists:profile')
