from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Artist, Demo
from ..forms import ArtistForm, DemoForm

@login_required
def artist_profile(request):
    """View for artist's own profile"""
    try:
        artist = request.user.artist
    except Artist.DoesNotExist:
        artist = None
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
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
