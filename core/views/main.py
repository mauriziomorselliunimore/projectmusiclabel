from django.shortcuts import render
from artists.models import Artist
from associates.models import Associate
from booking.models import Booking

def home(request):
    """
    Vista principale della homepage che mostra:
    - Ultimi artisti registrati
    - Professionisti in evidenza
    - Ultime prenotazioni (se l'utente è loggato)
    """
    context = {
        'latest_artists': Artist.objects.filter(is_active=True).order_by('-created_at')[:6],
        'featured_associates': Associate.objects.filter(is_active=True).order_by('?')[:6],
    }
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'artist'):
            # Se l'utente è un artista, mostra le sue prenotazioni
            context['recent_bookings'] = Booking.objects.filter(
                artist=request.user.artist
            ).order_by('-created_at')[:5]
        elif hasattr(request.user, 'associate'):
            # Se l'utente è un professionista, mostra le prenotazioni ricevute
            context['recent_bookings'] = Booking.objects.filter(
                associate=request.user.associate
            ).order_by('-created_at')[:5]
    
    return render(request, 'home.html', context)
