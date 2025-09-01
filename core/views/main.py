from django.shortcuts import render
from django.contrib.auth import get_user_model
from artists.models import Artist
from associates.models import Associate
from booking.models import Booking

__all__ = [
    'home',
    'populate_database',
    'clear_database',
    'create_superuser_render',
    'render_status',
]

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
            context['recent_bookings'] = Booking.objects.filter(
                artist=request.user.artist
            ).order_by('-created_at')[:5]
        elif hasattr(request.user, 'associate'):
            context['recent_bookings'] = Booking.objects.filter(
                associate=request.user.associate
            ).order_by('-created_at')[:5]
    
    return render(request, 'home.html', context)

def populate_database(request):
    """Popola il database con dati di esempio"""
    if not request.user.is_superuser:
        return render(request, 'admin/not_authorized.html')
    
    # Creiamo alcuni utenti di esempio
    User = get_user_model()
    # Artisti
    for i in range(1, 6):
        user = User.objects.create_user(
            username=f'artist{i}',
            email=f'artist{i}@example.com',
            password='password123'
        )
        Artist.objects.create(
            user=user,
            name=f'Artist {i}',
            genre=f'Genre {i}',
            bio=f'Bio for Artist {i}'
        )
    
    # Professionisti
    for i in range(1, 6):
        user = User.objects.create_user(
            username=f'associate{i}',
            email=f'associate{i}@example.com',
            password='password123'
        )
        Associate.objects.create(
            user=user,
            name=f'Associate {i}',
            profession=f'Profession {i}',
            bio=f'Bio for Associate {i}'
        )
    
    return render(request, 'admin/populate_success.html')

def clear_database(request):
    """Pulisce il database"""
    if not request.user.is_superuser:
        return render(request, 'admin/not_authorized.html')
    
    # Cancelliamo tutti i dati tranne l'utente admin
    Booking.objects.all().delete()
    Artist.objects.all().delete()
    Associate.objects.all().delete()
    User = get_user_model()
    User.objects.exclude(is_superuser=True).delete()
    
    return render(request, 'admin/clear_success.html')
    return render(request, 'admin/clear_success.html')

def create_superuser_render(request):
    """Crea un superuser per l'ambiente Render"""
    if not request.user.is_superuser:
        return render(request, 'admin/not_authorized.html')
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        admin.is_staff = True
        admin.save()
    return render(request, 'admin/superuser_success.html')

def render_status(request):
    """Mostra lo stato dell'ambiente Render"""
    if not request.user.is_superuser:
        return render(request, 'admin/not_authorized.html')
    context = {
        'status': 'ok',
        'environment': 'render',
        'database': 'connected',
    }
    return render(request, 'admin/render_status.html', context)
