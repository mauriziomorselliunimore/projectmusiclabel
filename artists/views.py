from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
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
    """Dettaglio singolo artista"""
    artist = get_object_or_404(Artist, pk=pk, is_active=True)
    demos = artist.demos.filter(is_public=True)
    
    context = {
        'artist': artist,
        'demos': demos,
        'is_owner': request.user == artist.user,
    }
    return render(request, 'artists/artist_detail.html', context)

@login_required
def artist_create(request):
    """Crea profilo artista"""
    # Check if user already has an artist profile
    if hasattr(request.user, 'artist'):
        messages.info(request, 'Hai già un profilo artista!')
        return redirect('artists:detail', pk=request.user.artist.pk)
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
            artist.save()
            messages.success(request, 'Profilo artista creato con successo!')
            return redirect('artists:detail', pk=artist.pk)
    else:
        form = ArtistForm()
    
    return render(request, 'artists/artist_form.html', {'form': form, 'title': 'Crea Profilo Artista'})

@login_required
def artist_edit(request, pk):
    """Modifica profilo artista"""
    artist = get_object_or_404(Artist, pk=pk)
    
    # Check ownership
    if artist.user != request.user:
        messages.error(request, 'Non hai i permessi per modificare questo profilo!')
        return redirect('artists:detail', pk=pk)
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('artists:detail', pk=pk)
    else:
        form = ArtistForm(instance=artist)
    
    return render(request, 'artists/artist_form.html', {'form': form, 'title': 'Modifica Profilo'})

@login_required
def demo_upload(request):
    """Upload demo musicale"""
    if not hasattr(request.user, 'artist'):
        messages.error(request, 'Devi avere un profilo artista per caricare demo!')
        return redirect('artists:create')
    
    if request.method == 'POST':
        form = DemoForm(request.POST, request.FILES)
        if form.is_valid():
            demo = form.save(commit=False)
            demo.artist = request.user.artist
            demo.save()
            messages.success(request, f'Demo "{demo.title}" caricata con successo!')
            return redirect('artists:detail', pk=request.user.artist.pk)
    else:
        form = DemoForm()
    
    return render(request, 'artists/demo_form.html', {'form': form})

@login_required
def demo_delete(request, pk):
    """Elimina demo"""
    demo = get_object_or_404(Demo, pk=pk)
    
    # Check ownership
    if demo.artist.user != request.user:
        messages.error(request, 'Non hai i permessi per eliminare questa demo!')
        return redirect('artists:detail', pk=demo.artist.pk)
    
    if request.method == 'POST':
        demo.delete()
        messages.success(request, 'Demo eliminata con successo!')
        return redirect('artists:detail', pk=demo.artist.pk)
    
    return render(request, 'artists/demo_confirm_delete.html', {'demo': demo})