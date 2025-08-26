from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from accounts.models import Profile
import random

def home(request):
    """Homepage con statistiche e link rapidi"""
    # Statistiche per la homepage
    stats = {
        'total_artists': Artist.objects.filter(is_active=True).count(),
        'total_associates': Associate.objects.filter(is_active=True).count(),
        'total_demos': Demo.objects.filter(is_public=True).count(),
        'latest_artists': Artist.objects.filter(is_active=True)[:3],
        'latest_associates': Associate.objects.filter(is_active=True, is_available=True)[:3],
    }
    return render(request, 'home.html', stats)

@user_passes_test(lambda u: u.is_superuser)
def populate_database(request):
    """Popola il database con dati di esempio"""
    try:
        with transaction.atomic():
            # Dati di esempio per artisti
            artists_data = [
                {
                    'username': 'marco_blues',
                    'email': 'marco@example.com',
                    'first_name': 'Marco',
                    'last_name': 'Rossi',
                    'stage_name': 'Blues Marco',
                    'genres': 'Blues, Rock, Jazz',
                    'bio': 'Chitarrista blues con 15 anni di esperienza. Ho suonato in numerosi club di Roma e Milano.',
                    'location': 'Roma, Italia',
                    'phone': '+39 333 111 2222',
                    'spotify_url': 'https://open.spotify.com/artist/marco-blues',
                    'instagram_url': 'https://instagram.com/marcoblues',
                },
                {
                    'username': 'sofia_pop',
                    'email': 'sofia@example.com', 
                    'first_name': 'Sofia',
                    'last_name': 'Bianchi',
                    'stage_name': 'Sofia B',
                    'genres': 'Pop, R&B, Soul',
                    'bio': 'Cantante pop emergente. Ho partecipato a X Factor 2023 e sto lavorando al mio primo album.',
                    'location': 'Milano, Italia',
                    'phone': '+39 333 333 4444',
                    'youtube_url': 'https://youtube.com/c/sofiabmusic',
                    'instagram_url': 'https://instagram.com/sofiab_official',
                },
                {
                    'username': 'dj_elektro',
                    'email': 'alessandro@example.com',
                    'first_name': 'Alessandro',
                    'last_name': 'Verdi',
                    'stage_name': 'DJ Elektro',
                    'genres': 'Electronic, House, Techno',
                    'bio': 'Producer e DJ elettronico. Le mie tracce sono state suonate nei migliori club europei.',
                    'location': 'Napoli, Italia',
                    'phone': '+39 333 555 6666',
                    'soundcloud_url': 'https://soundcloud.com/dj-elektro',
                    'spotify_url': 'https://open.spotify.com/artist/dj-elektro',
                }
            ]

            # Dati di esempio per associati
            associates_data = [
                {
                    'username': 'luca_sound',
                    'email': 'luca@example.com',
                    'first_name': 'Luca',
                    'last_name': 'Ferrari',
                    'specialization': 'Sound Engineer',
                    'skills': 'Pro Tools, Logic Pro, Mixing, Mastering, Live Sound',
                    'experience_level': 'professional',
                    'hourly_rate': 45.00,
                    'bio': 'Fonico professionista con 10+ anni di esperienza. Ho lavorato con artisti nazionali e internazionali.',
                    'location': 'Roma, Italia',
                    'phone': '+39 333 777 8888',
                    'availability': 'Lunedì-Venerdì 9-18, Weekend su richiesta',
                    'years_experience': 12,
                    'website': 'https://lucastudio.com',
                },
                {
                    'username': 'anna_producer',
                    'email': 'anna@example.com',
                    'first_name': 'Anna',
                    'last_name': 'Romano',
                    'specialization': 'Music Producer',
                    'skills': 'Ableton Live, Composizione, Arrangiamento, Beat Making',
                    'experience_level': 'advanced',
                    'hourly_rate': 35.00,
                    'bio': 'Producer specializzata in pop e hip-hop. Ho prodotto oltre 50 singoli negli ultimi 3 anni.',
                    'location': 'Milano, Italia',
                    'phone': '+39 333 999 0000',
                    'availability': 'Flessibile, anche sere e weekend',
                    'years_experience': 7,
                },
                {
                    'username': 'giuseppe_drummer',
                    'email': 'giuseppe@example.com',
                    'first_name': 'Giuseppe',
                    'last_name': 'Conti',
                    'specialization': 'Session Drummer',
                    'skills': 'Batteria acustica, Elettronica, Recording, Live Performance',
                    'experience_level': 'professional',
                    'hourly_rate': 40.00,
                    'bio': 'Batterista session con esperienza in rock, pop e jazz. Disponibile per registrazioni e live.',
                    'location': 'Torino, Italia',
                    'phone': '+39 333 111 2223',
                    'availability': 'Da concordare',
                    'years_experience': 15,
                }
            ]

            created_artists = 0
            created_associates = 0

            # Crea artisti
            for data in artists_data:
                # Estrai dati user
                user_data = {
                    'username': data.pop('username'),
                    'email': data.pop('email'),
                    'first_name': data.pop('first_name'),
                    'last_name': data.pop('last_name'),
                }
                
                # Crea user se non esiste
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults=user_data
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    # Crea profilo
                    Profile.objects.create(user=user, user_type='artist')
                    
                    # Crea artista
                    Artist.objects.create(user=user, **data)
                    created_artists += 1

            # Crea associati
            for data in associates_data:
                # Estrai dati user
                user_data = {
                    'username': data.pop('username'),
                    'email': data.pop('email'),
                    'first_name': data.pop('first_name'),
                    'last_name': data.pop('last_name'),
                }
                
                # Crea user se non esiste
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults=user_data
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    # Crea profilo
                    Profile.objects.create(user=user, user_type='associate')
                    
                    # Crea associato
                    Associate.objects.create(user=user, **data)
                    created_associates += 1

            # Crea alcune demo di esempio
            demo_titles = [
                "Midnight Blues", "Electric Dreams", "Summer Vibes", 
                "Rock Revolution", "Soul Connection", "Urban Beat"
            ]
            
            artists = Artist.objects.all()
            created_demos = 0
            
            for artist in artists:
                for i in range(2):  # 2 demo per artista
                    if demo_titles:
                        title = demo_titles.pop(0)
                        Demo.objects.get_or_create(
                            artist=artist,
                            title=title,
                            defaults={
                                'genre': random.choice(['rock', 'pop', 'blues', 'electronic']),
                                'description': f'Demo "{title}" di {artist.stage_name}',
                                'duration': f"{random.randint(2,5)}:{random.randint(10,59):02d}",
                                'is_public': True,
                            }
                        )
                        created_demos += 1

            messages.success(
                request,
                f'Database popolato! Creati: {created_artists} artisti, {created_associates} associati, {created_demos} demo'
            )
            
    except Exception as e:
        messages.error(request, f'Errore nel popolamento: {str(e)}')
    
    return redirect('core:home')

@user_passes_test(lambda u: u.is_superuser)
def clear_database(request):
    """Svuota il database (solo per admin)"""
    try:
        with transaction.atomic():
            Demo.objects.all().delete()
            PortfolioItem.objects.all().delete()
            Artist.objects.all().delete()
            Associate.objects.all().delete()
            Profile.objects.all().delete()
            # Non eliminiamo gli utenti admin
            User.objects.filter(is_superuser=False).delete()
            
        messages.success(request, 'Database svuotato con successo!')
    except Exception as e:
        messages.error(request, f'Errore nello svuotamento: {str(e)}')
    
    return redirect('core:home')