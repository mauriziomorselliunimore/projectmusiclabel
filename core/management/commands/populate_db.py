from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Popola il database con dati di esempio'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('🎵 Creazione artisti di esempio...')
            
            # Lista degli artisti
            artists_data = [
                {
                    'username': 'marco_rossi',
                    'email': 'marco.rossi@example.com',
                    'password': 'testpass123',
                    'first_name': 'Marco',
                    'last_name': 'Rossi',
                    'artist': {
                        'stage_name': 'MR Wave',
                        'genre': 'Rock',
                        'bio': 'Cantautore rock con influenze indie e alternative',
                        'city': 'Milano'
                    }
                },
                {
                    'username': 'laura_bianchi',
                    'email': 'laura.bianchi@example.com',
                    'password': 'testpass123',
                    'first_name': 'Laura',
                    'last_name': 'Bianchi',
                    'artist': {
                        'stage_name': 'LauraB',
                        'genre': 'Pop',
                        'bio': 'Cantante pop con un tocco di soul',
                        'city': 'Roma'
                    }
                },
                {
                    'username': 'giovanni_verdi',
                    'email': 'giovanni.verdi@example.com',
                    'password': 'testpass123',
                    'first_name': 'Giovanni',
                    'last_name': 'Verdi',
                    'artist': {
                        'stage_name': 'DJ Verde',
                        'genre': 'Electronic',
                        'bio': 'DJ e produttore di musica elettronica',
                        'city': 'Torino'
                    }
                }
            ]

            # Creazione artisti
            for artist_data in artists_data:
                # Crea utente
                user = User.objects.create_user(
                    username=artist_data['username'],
                    email=artist_data['email'],
                    password=artist_data['password'],
                    first_name=artist_data['first_name'],
                    last_name=artist_data['last_name']
                )
                
                # Crea artista
                artist = Artist.objects.create(
                    user=user,
                    stage_name=artist_data['artist']['stage_name'],
                    genre=artist_data['artist']['genre'],
                    bio=artist_data['artist']['bio'],
                    city=artist_data['artist']['city'],
                    slug=slugify(artist_data['artist']['stage_name'])
                )
                
                # Crea demo di esempio
                Demo.objects.create(
                    artist=artist,
                    title=f'Demo {artist.stage_name}',
                    description=f'Demo di presentazione di {artist.stage_name}',
                    genre=artist.genre
                )

            self.stdout.write('👔 Creazione professionisti di esempio...')
            
            # Lista dei professionisti
            associates_data = [
                {
                    'username': 'studio_sound',
                    'email': 'info@studiosound.com',
                    'password': 'testpass123',
                    'first_name': 'Paolo',
                    'last_name': 'Neri',
                    'associate': {
                        'company_name': 'Studio Sound',
                        'type': 'recording_studio',
                        'bio': 'Studio di registrazione professionale con 20 anni di esperienza',
                        'city': 'Milano',
                        'portfolio_items': [
                            {
                                'title': 'Studio A',
                                'description': 'Studio principale con attrezzatura analogica vintage'
                            },
                            {
                                'title': 'Studio B',
                                'description': 'Studio digitale per produzioni moderne'
                            }
                        ]
                    }
                },
                {
                    'username': 'talent_scout',
                    'email': 'mario.talent@example.com',
                    'password': 'testpass123',
                    'first_name': 'Mario',
                    'last_name': 'Talenti',
                    'associate': {
                        'company_name': 'Talent Scout Agency',
                        'type': 'manager',
                        'bio': 'Agenzia di talent scouting e management artisti',
                        'city': 'Roma',
                        'portfolio_items': [
                            {
                                'title': 'Scoperte 2024',
                                'description': 'Artisti emergenti scoperti e lanciati nel 2024'
                            }
                        ]
                    }
                },
                {
                    'username': 'promo_events',
                    'email': 'eventi@promoevents.com',
                    'password': 'testpass123',
                    'first_name': 'Anna',
                    'last_name': 'Eventi',
                    'associate': {
                        'company_name': 'PromoEvents',
                        'type': 'promoter',
                        'bio': 'Organizzazione eventi e promozione artisti',
                        'city': 'Bologna',
                        'portfolio_items': [
                            {
                                'title': 'Festival Estate 2024',
                                'description': 'Festival musicale con oltre 30 artisti'
                            },
                            {
                                'title': 'Club Tour 2024',
                                'description': 'Tour nei migliori club italiani'
                            }
                        ]
                    }
                }
            ]
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