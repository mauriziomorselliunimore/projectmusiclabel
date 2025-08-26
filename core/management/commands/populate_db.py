# File: core/management/commands/populate_db.py
# Crea le cartelle: core/management/ e core/management/commands/
# Aggiungi __init__.py in entrambe le cartelle

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from accounts.models import Profile
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
import random

class Command(BaseCommand):
    help = 'Popola il database con dati di esempio'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('🎵 Popolamento database in corso...')
            
            # Dati artisti
            artists_data = [
                {
                    'user_data': {'username': 'marco_blues', 'email': 'marco@example.com', 'first_name': 'Marco', 'last_name': 'Rossi'},
                    'artist_data': {
                        'stage_name': 'Blues Marco',
                        'genres': 'Blues, Rock, Jazz',
                        'bio': 'Chitarrista blues con 15 anni di esperienza nel circuito romano.',
                        'location': 'Roma, Italia',
                        'phone': '+39 333 111 2222',
                        'spotify_url': 'https://open.spotify.com/artist/marco-blues',
                        'instagram_url': 'https://instagram.com/marcoblues',
                    }
                },
                {
                    'user_data': {'username': 'sofia_pop', 'email': 'sofia@example.com', 'first_name': 'Sofia', 'last_name': 'Bianchi'},
                    'artist_data': {
                        'stage_name': 'Sofia B',
                        'genres': 'Pop, R&B, Soul',
                        'bio': 'Cantante pop emergente, finalista X Factor 2023.',
                        'location': 'Milano, Italia',
                        'phone': '+39 333 333 4444',
                        'youtube_url': 'https://youtube.com/c/sofiabmusic',
                        'instagram_url': 'https://instagram.com/sofiab_official',
                    }
                },
                {
                    'user_data': {'username': 'dj_elektro', 'email': 'alessandro@example.com', 'first_name': 'Alessandro', 'last_name': 'Verdi'},
                    'artist_data': {
                        'stage_name': 'DJ Elektro',
                        'genres': 'Electronic, House, Techno',
                        'bio': 'Producer elettronico con residency nei migliori club europei.',
                        'location': 'Napoli, Italia',
                        'phone': '+39 333 555 6666',
                        'soundcloud_url': 'https://soundcloud.com/dj-elektro',
                        'spotify_url': 'https://open.spotify.com/artist/dj-elektro',
                    }
                }
            ]

            # Dati associati
            associates_data = [
                {
                    'user_data': {'username': 'luca_sound', 'email': 'luca@example.com', 'first_name': 'Luca', 'last_name': 'Ferrari'},
                    'associate_data': {
                        'specialization': 'Sound Engineer',
                        'skills': 'Pro Tools, Logic Pro, Mixing, Mastering, Live Sound',
                        'experience_level': 'professional',
                        'hourly_rate': 45.00,
                        'bio': 'Fonico professionista con 10+ anni di esperienza nazionale e internazionale.',
                        'location': 'Roma, Italia',
                        'phone': '+39 333 777 8888',
                        'availability': 'Lunedì-Venerdì 9-18, Weekend su richiesta',
                        'years_experience': 12,
                        'website': 'https://lucastudio.com',
                    }
                },
                {
                    'user_data': {'username': 'anna_producer', 'email': 'anna@example.com', 'first_name': 'Anna', 'last_name': 'Romano'},
                    'associate_data': {
                        'specialization': 'Music Producer',
                        'skills': 'Ableton Live, Composizione, Arrangiamento, Beat Making',
                        'experience_level': 'advanced',
                        'hourly_rate': 35.00,
                        'bio': 'Producer specializzata in pop e hip-hop. Oltre 50 singoli prodotti.',
                        'location': 'Milano, Italia',
                        'phone': '+39 333 999 0000',
                        'availability': 'Flessibile, anche sere e weekend',
                        'years_experience': 7,
                    }
                },
            ]

            created_artists = 0
            created_associates = 0
            created_demos = 0

            # Crea artisti
            for data in artists_data:
                user, created = User.objects.get_or_create(
                    username=data['user_data']['username'],
                    defaults=data['user_data']
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    # Crea profile
                    Profile.objects.create(user=user, user_type='artist')
                    
                    # Crea artist
                    Artist.objects.create(user=user, **data['artist_data'])
                    created_artists += 1

            # Crea associati
            for data in associates_data:
                user, created = User.objects.get_or_create(
                    username=data['user_data']['username'],
                    defaults=data['user_data']
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    # Crea profile
                    Profile.objects.create(user=user, user_type='associate')
                    
                    # Crea associate
                    Associate.objects.create(user=user, **data['associate_data'])
                    created_associates += 1

            # Crea demo di esempio
            demo_data = [
                {'title': 'Midnight Blues', 'genre': 'blues', 'description': 'Un blues notturno che racconta storie di vita.'},
                {'title': 'Electric Dreams', 'genre': 'electronic', 'description': 'Viaggio sonoro nella musica elettronica moderna.'},
                {'title': 'Summer Vibes', 'genre': 'pop', 'description': 'Brano pop perfetto per l\'estate.'},
                {'title': 'Rock Revolution', 'genre': 'rock', 'description': 'Rock energico con riff potenti.'},
                {'title': 'Soul Connection', 'genre': 'r&b', 'description': 'R&B moderno con influenze soul.'},
                {'title': 'Urban Beat', 'genre': 'hip-hop', 'description': 'Hip-hop urbano con beat coinvolgenti.'},
            ]

            artists = Artist.objects.all()
            for artist in artists:
                for i in range(2):  # 2 demo per artista
                    if demo_data:
                        demo_info = demo_data.pop(0)
                        Demo.objects.get_or_create(
                            artist=artist,
                            title=demo_info['title'],
                            defaults={
                                'genre': demo_info['genre'],
                                'description': demo_info['description'],
                                'duration': f"{random.randint(2,5)}:{random.randint(10,59):02d}",
                                'is_public': True,
                            }
                        )
                        created_demos += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Popolamento completato!\n'
                    f'   📱 Artisti creati: {created_artists}\n'
                    f'   🔧 Associati creati: {created_associates}\n'
                    f'   🎵 Demo create: {created_demos}'
                )
            )