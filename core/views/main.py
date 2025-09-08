from django.shortcuts import render
from django.contrib.auth import get_user_model
from artists.models import Artist
from associates.models import Associate
from booking.models import Booking
from accounts.models import Profile

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
    - Statistiche generali
    """
    # Ottieni gli ultimi artisti e professionisti
    latest_artists = Artist.objects.filter(is_active=True).order_by('-created_at')[:6]
    featured_associates = Associate.objects.filter(is_active=True).order_by('?')[:6]
    
    # Calcola le statistiche
    from artists.models import Demo
    context = {
        'latest_artists': latest_artists,
        'featured_associates': featured_associates,
        'total_artists': Artist.objects.filter(is_active=True).count() or 0,
        'total_associates': Associate.objects.filter(is_active=True).count() or 0,
        'total_demos': Demo.objects.filter(is_public=True).count() or 0,
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
            'first_name': 'Marco',
            'last_name': 'Bianchi',
            'email': 'marco@example.com',
            'stage_name': 'Marco Blues',
            'genres': 'blues, rock',
            'bio': 'Cantante e chitarrista blues con 10 anni di esperienza',
            'location': 'Milano, Italia',
            'demos': [
                {
                    'title': 'Blues in A',
                    'genre': 'blues',
                    'description': 'Blues classico con chitarra slide registrato live al Blue Note',
                    'external_audio_url': 'https://soundcloud.com/blues-rock/blues-in-a-live',
                    'duration': '4:35',
                    'is_public': True
                },
                {
                    'title': 'Rock Fusion',
                    'genre': 'rock',
                    'description': 'Fusione di blues e rock moderno con influenze psichedeliche',
                    'external_audio_url': 'https://www.youtube.com/watch?v=rock-fusion-demo',
                    'duration': '5:15',
                    'is_public': True
                },
                {
                    'title': 'Midnight Train',
                    'genre': 'blues',
                    'description': 'Un blues notturno ispirato ai viaggi in treno',
                    'external_audio_url': 'https://open.spotify.com/track/midnight-train-blues',
                    'duration': '6:20',
                    'is_public': True
                }
            ]
        },
        {
            'username': 'sara_jazz',
            'first_name': 'Sara',
            'last_name': 'Rossi',
            'email': 'sara@example.com',
            'stage_name': 'Sara Soul',
            'genres': 'jazz, r&b',
            'bio': 'Cantante jazz con influenze soul e R&B',
            'location': 'Roma, Italia',
            'demos': [
                {
                    'title': 'Jazz Standards Medley',
                    'genre': 'jazz',
                    'description': 'Medley di classici jazz reinterpretati con arrangiamenti moderni',
                    'external_audio_url': 'https://soundcloud.com/jazz-soul/standards-medley',
                    'duration': '7:45',
                    'is_public': True
                },
                {
                    'title': 'Soul Session Live',
                    'genre': 'r&b',
                    'description': 'Session live registrata al Jazz Club con band completa',
                    'external_audio_url': 'https://www.youtube.com/watch?v=soul-session-live',
                    'duration': '8:30',
                    'is_public': True
                },
                {
                    'title': 'Bossa Nova Experiment',
                    'genre': 'jazz',
                    'description': 'Fusione di jazz e bossa nova con elementi elettronici',
                    'external_audio_url': 'https://open.spotify.com/track/bossa-nova-exp',
                    'duration': '5:55',
                    'is_public': True
                }
            ]
        }
    ]
    
    # Professionisti con i loro portfolio
    associate_data = [
        {
            'username': 'luca_sound',
            'first_name': 'Luca',
            'last_name': 'Verdi',
            'email': 'luca@example.com',
            'specialization': 'Sound Engineer',
            'skills': 'sound-engineer, mixing, mastering',
            'experience_level': 'professional',
            'hourly_rate': '50.00',
            'availability': 'Lunedì-Venerdì, 9:00-18:00',
            'bio': 'Tecnico del suono con esperienza in studio e live',
            'location': 'Milano, Italia',
            'website': 'https://lucaverdi.it',
            'portfolio_description': 'Specializzato in registrazione, mix e mastering per progetti musicali di ogni genere',
            'portfolios': [
                {'title': 'Studio Mix', 'description': 'Mix e mastering per album jazz'},
                {'title': 'Live Sound', 'description': 'Gestione audio per concerti dal vivo'}
            ]
        },
        {
            'username': 'anna_producer',
            'first_name': 'Anna',
            'last_name': 'Neri',
            'email': 'anna@example.com',
            'specialization': 'Music Producer',
            'skills': 'producer, mixing, arranging',
            'experience_level': 'professional',
            'hourly_rate': '60.00',
            'availability': 'Flessibile, anche weekend',
            'bio': 'Produttrice musicale specializzata in musica elettronica',
            'location': 'Roma, Italia',
            'website': 'https://annaneri.it',
            'portfolio_description': 'Produttrice con focus su elettronica e sound design moderno',
            'portfolios': [
                {'title': 'EDM Production', 'description': 'Produzione di tracce EDM'},
                {'title': 'Remix Work', 'description': 'Remix per artisti internazionali'}
            ]
        }
    ]

    # Crea artisti e i loro demo
    for data in artist_data:
        # Crea l'utente solo se non esiste
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'password': 'password123',
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if not created:
            # Aggiorna i dati se necessario
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.set_password('password123')
            user.save()
        # Crea l'artista
        artist = Artist.objects.get_or_create(
            user=user,
            defaults={
                'stage_name': data['stage_name'],
                'genres': data['genres'],
                'bio': data['bio'],
                'location': data['location'],
                'is_active': True
            }
        )[0]
        # Crea le demo
        for demo in data['demos']:
            from artists.models import Demo
            Demo.objects.get_or_create(
                artist=artist,
                title=demo['title'],
                genre=demo['genre'],
                defaults={
                    'description': demo['description'],
                    'external_audio_url': demo['external_audio_url'],
                    'duration': demo['duration'],
                    'is_public': demo['is_public']
                }
            )

    # Crea professionisti e i loro portfolio
    for data in associate_data:
        # Crea l'utente solo se non esiste
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'password': 'password123',
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
    # Aggiorna sempre la password per sicurezza
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.set_password('password123')
    user.save()
        # Crea il profilo del professionista
        from accounts.models import Profile
        Profile.objects.get_or_create(user=user, defaults={'user_type': 'associate'})

        # Crea il professionista
        associate = Associate.objects.create(
            user=user,
            specialization=data['specialization'],
            skills=data['skills'],
            experience_level=data['experience_level'],
            hourly_rate=data['hourly_rate'],
            availability=data['availability'],
            bio=data['bio'],
            location=data['location'],
            website=data['website'],
            portfolio_description=data['portfolio_description']
        )

        # Crea i portfolio items
        for portfolio in data['portfolios']:
            from associates.models import PortfolioItem
            PortfolioItem.objects.create(
                associate=associate,
                title=portfolio['title'],
                description=portfolio['description'],
                external_url='https://example.com/portfolio/' + portfolio['title'].lower().replace(' ', '-')
            )
    
    return render(request, 'admin/populate_success.html')

def clear_database(request):
    """Pulisce il database"""
    if not request.user.is_superuser:
        return render(request, 'admin/not_authorized.html')
    
    # Cancelliamo tutti i dati tranne l'utente admin
    from django.db import ProgrammingError
    try:
        Booking.objects.all().delete()
        Artist.objects.all().delete()
        Associate.objects.all().delete()
        User = get_user_model()
        User.objects.exclude(is_superuser=True).delete()
    except ProgrammingError as e:
        # Logga l'errore e continua
        print(f"Errore durante la cancellazione: {e}")
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
