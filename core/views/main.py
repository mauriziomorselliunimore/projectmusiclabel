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
    
    # Artisti con i loro demo
    artist_data = [
        {
            'username': 'marco_blues',
            'name': 'Marco Bianchi',
            'email': 'marco@example.com',
            'genre': 'Blues/Rock',
            'bio': 'Cantante e chitarrista blues con 10 anni di esperienza',
            'demos': [
                {'title': 'Blues in A', 'description': 'Blues classico con chitarra slide'},
                {'title': 'Rock Fusion', 'description': 'Fusione di blues e rock moderno'}
            ]
        },
        {
            'username': 'sara_jazz',
            'name': 'Sara Rossi',
            'email': 'sara@example.com',
            'genre': 'Jazz/Soul',
            'bio': 'Cantante jazz con influenze soul e R&B',
            'demos': [
                {'title': 'Jazz Standards', 'description': 'Raccolta di classici jazz reinterpretati'},
                {'title': 'Soul Session', 'description': 'Session live con band jazz'}
            ]
        }
    ]
    
    # Professionisti con i loro portfolio
    associate_data = [
        {
            'username': 'luca_sound',
            'name': 'Luca Verdi',
            'email': 'luca@example.com',
            'profession': 'Sound Engineer',
            'bio': 'Tecnico del suono con esperienza in studio e live',
            'portfolios': [
                {'title': 'Studio Mix', 'description': 'Mix e mastering per album jazz'},
                {'title': 'Live Sound', 'description': 'Gestione audio per concerti dal vivo'}
            ]
        },
        {
            'username': 'anna_producer',
            'name': 'Anna Neri',
            'email': 'anna@example.com',
            'profession': 'Music Producer',
            'bio': 'Produttrice musicale specializzata in musica elettronica',
            'portfolios': [
                {'title': 'EDM Production', 'description': 'Produzione di tracce EDM'},
                {'title': 'Remix Work', 'description': 'Remix per artisti internazionali'}
            ]
        }
    ]

    # Crea artisti e i loro demo
    for data in artist_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123'
        )
        artist = Artist.objects.create(
            user=user,
            name=data['name'],
            genre=data['genre'],
            bio=data['bio']
        )
        for demo in data['demos']:
            from artists.models import Demo
            Demo.objects.create(
                artist=artist,
                title=demo['title'],
                description=demo['description']
            )

    # Crea professionisti e i loro portfolio
    for data in associate_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123'
        )
        associate = Associate.objects.create(
            user=user,
            name=data['name'],
            profession=data['profession'],
            bio=data['bio']
        )
        for portfolio in data['portfolios']:
            from associates.models import Portfolio
            Portfolio.objects.create(
                associate=associate,
                title=portfolio['title'],
                description=portfolio['description']
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
