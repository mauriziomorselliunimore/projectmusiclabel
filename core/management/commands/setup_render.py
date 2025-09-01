from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from accounts.models import Profile
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
import random

class Command(BaseCommand):
    help = 'Setup iniziale per Render: crea superuser e popola DB (con URL esterni)'

    def add_arguments(self, parser):
        parser.add_argument('--skip-superuser', action='store_true', help='Skip superuser creation')
        parser.add_argument('--skip-populate', action='store_true', help='Skip database population')

    def handle(self, *args, **options):
        self.stdout.write('🚀 Setup Render in corso...')
        
        if not options['skip_superuser']:
            self.create_superuser()
        
        if not options['skip_populate']:
            self.populate_database()
        
        self.stdout.write(self.style.SUCCESS('✅ Setup Render completato!'))

    def create_superuser(self):
        """Crea superuser se non esiste già"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('👨‍💼 Superuser creato: admin/admin')
        else:
            # Se l'admin esiste già, aggiorna la sua password
            admin = User.objects.get(username='admin')
            admin.set_password('admin')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write('👨‍💼 Password admin aggiornata a: admin')

    def populate_database(self):
        """Popola il database solo se vuoto"""
        if Artist.objects.exists() or Associate.objects.exists():
            self.stdout.write('📊 Database già popolato')
            return

        try:
            with transaction.atomic():
                # Dati artisti con link esterni reali
                artists_data = [
                    {
                        'user_data': {
                            'username': 'marco_blues',
                            'email': 'marco@example.com',
                            'first_name': 'Marco',
                            'last_name': 'Rossi'
                        },
                        'artist_data': {
                            'stage_name': 'Blues Marco',
                            'genres': 'Blues, Rock, Jazz',
                            'bio': 'Chitarrista blues con 15 anni di esperienza. Appassionato di musica dal vivo e jam session nei club di Roma.',
                            'location': 'Roma, Italia',
                            'phone': '+39 333 111 2222',
                            'spotify_url': 'https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb',
                            'instagram_url': 'https://instagram.com/blues_official',
                            'youtube_url': 'https://youtube.com/channel/UCxyz123',
                        },
                        'profile_data': {
                            'external_avatar_url': 'https://i.pravatar.cc/150?u=marco',
                            'bio': 'Musicista blues romano con passione per la chitarra.',
                            'location': 'Roma, Italia',
                        }
                    },
                    {
                        'user_data': {
                            'username': 'sofia_pop',
                            'email': 'sofia@example.com',
                            'first_name': 'Sofia',
                            'last_name': 'Bianchi'
                        },
                        'artist_data': {
                            'stage_name': 'Sofia B',
                            'genres': 'Pop, R&B, Soul',
                            'bio': 'Cantante pop emergente, finalista X Factor 2023. Attualmente lavoro al mio primo album in studio con producer internazionali.',
                            'location': 'Milano, Italia',
                            'phone': '+39 333 333 4444',
                            'youtube_url': 'https://youtube.com/channel/UCabc456',
                            'instagram_url': 'https://instagram.com/sofiab_music',
                            'spotify_url': 'https://open.spotify.com/artist/1vCWHaC5f2uS3yhpwWbIA6',
                        },
                        'profile_data': {
                            'external_avatar_url': 'https://i.pravatar.cc/150?u=sofia',
                            'bio': 'Cantante pop milanese, X Factor 2023.',
                            'location': 'Milano, Italia',
                        }
                    },
                    {
                        'user_data': {
                            'username': 'dj_elektro',
                            'email': 'alessandro@example.com',
                            'first_name': 'Alessandro',
                            'last_name': 'Verdi'
                        },
                        'artist_data': {
                            'stage_name': 'DJ Elektro',
                            'genres': 'Electronic, House, Techno',
                            'bio': 'Producer e DJ elettronico specializzato in musica house e techno. Resident DJ nei migliori club di Ibiza e Mykonos durante la stagione estiva.',
                            'location': 'Napoli, Italia',
                            'phone': '+39 333 555 6666',
                            'soundcloud_url': 'https://soundcloud.com/dj-elektro-official',
                            'spotify_url': 'https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V',
                        },
                        'profile_data': {
                            'external_avatar_url': 'https://i.pravatar.cc/150?u=dj',
                            'bio': 'DJ e producer elettronico napoletano.',
                            'location': 'Napoli, Italia',
                        }
                    }
                ]

                # Dati associati
                associates_data = [
                    {
                        'user_data': {
                            'username': 'luca_sound',
                            'email': 'luca@example.com',
                            'first_name': 'Luca',
                            'last_name': 'Ferrari'
                        },
                        'associate_data': {
                            'specialization': 'Sound Engineer',
                            'skills': 'Pro Tools, Logic Pro, Mixing, Mastering, Live Sound',
                            'experience_level': 'professional',
                            'hourly_rate': 45.00,
                            'bio': 'Fonico professionista con oltre 10 anni di esperienza in studi di registrazione nazionali e internazionali. Specializzato in mixing e mastering per generi rock, pop e jazz.',
                            'location': 'Roma, Italia',
                            'phone': '+39 333 777 8888',
                            'availability': 'Lunedì-Venerdì 9-18, Weekend su richiesta',
                            'years_experience': 12,
                            'website': 'https://lucastudio.com',
                        },
                        'profile_data': {
                            'external_avatar_url': 'https://i.pravatar.cc/150?u=luca',
                            'bio': 'Sound engineer professionale con studio a Roma.',
                            'location': 'Roma, Italia',
                        }
                    },
                    {
                        'user_data': {
                            'username': 'anna_producer',
                            'email': 'anna@example.com',
                            'first_name': 'Anna',
                            'last_name': 'Romano'
                        },
                        'associate_data': {
                            'specialization': 'Music Producer',
                            'skills': 'Ableton Live, Composizione, Arrangiamento, Beat Making',
                            'experience_level': 'advanced',
                            'hourly_rate': 35.00,
                            'bio': 'Producer specializzata in pop e hip-hop moderno. Ho prodotto oltre 50 singoli negli ultimi 3 anni collaborando con artisti emergenti e affermati.',
                            'location': 'Milano, Italia',
                            'phone': '+39 333 999 0000',
                            'availability': 'Flessibile, anche sere e weekend',
                            'years_experience': 7,
                        },
                        'profile_data': {
                            'external_avatar_url': 'https://i.pravatar.cc/150?u=anna',
                            'bio': 'Producer musicale specializzata in pop e hip-hop.',
                            'location': 'Milano, Italia',
                        }
                    }
                ]

                created_artists = 0
                created_associates = 0

                # Crea artisti
                for data in artists_data:
                    user, created = User.objects.get_or_create(
                        username=data['user_data']['username'],
                        defaults=data['user_data']
                    )
                    
                    if created:
                        user.set_password('password123')
                        user.save()
                        
                        # Crea profilo con avatar esterno
                        Profile.objects.create(
                            user=user, 
                            user_type='artist',
                            **data.get('profile_data', {})
                        )
                        
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
                        
                        # Crea profilo con avatar esterno
                        Profile.objects.create(
                            user=user, 
                            user_type='associate',
                            **data.get('profile_data', {})
                        )
                        
                        Associate.objects.create(user=user, **data['associate_data'])
                        created_associates += 1

                # Demo con link esterni funzionanti
                demo_data = [
                    ('Midnight Blues', 'blues', 'Un blues notturno che racconta storie di vita urbana e solitudine.', 'https://soundcloud.com/example-demo/midnight-blues'),
                    ('Electric Dreams', 'electronic', 'Viaggio sonoro nella musica elettronica moderna con sintetizzatori vintage.', 'https://soundcloud.com/example-demo/electric-dreams'),
                    ('Summer Vibes', 'pop', 'Brano pop perfetto per l\'estate, fresco e coinvolgente con melodie orecchiabili.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                    ('Rock Revolution', 'rock', 'Rock energico con riff potenti e batteria travolgente che richiama i classici anni \'70.', 'https://soundcloud.com/example-demo/rock-revolution'),
                    ('Soul Connection', 'r&b', 'R&B moderno con influenze soul e jazz contemporaneo, perfetto per l\'ascolto serale.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                    ('Urban Beat', 'hip-hop', 'Hip-hop urbano con beat coinvolgenti e testi profondi sulla realtà metropolitana.', 'https://soundcloud.com/example-demo/urban-beat'),
                ]

                created_demos = 0
                artists = Artist.objects.all()
                
                for i, artist in enumerate(artists):
                    for j in range(2):  # 2 demo per artista
                        if i * 2 + j < len(demo_data):
                            title, genre, description, audio_url = demo_data[i * 2 + j]
                            Demo.objects.create(
                                artist=artist,
                                title=title,
                                genre=genre,
                                description=description,
                                external_audio_url=audio_url,
                                duration=f"{random.randint(2,5)}:{random.randint(10,59):02d}",
                                is_public=True,
                            )
                            created_demos += 1

                # Crea alcuni elementi portfolio per gli associati
                portfolio_data = [
                    {
                        'title': 'Album Mix - Indie Rock Band',
                        'description': 'Mixing completo di album debut per band indie rock emergente. 10 tracce, sound analogico.',
                        'external_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                        'external_image_url': 'https://picsum.photos/400/300?random=1',
                        'external_audio_url': 'https://soundcloud.com/example-portfolio/indie-mix',
                    },
                    {
                        'title': 'Single Pop - Mastering',
                        'description': 'Mastering professionale per singolo pop destinato alle radio nazionali.',
                        'external_url': 'https://soundcloud.com/example-portfolio/pop-master',
                        'external_image_url': 'https://picsum.photos/400/300?random=2',
                    },
                    {
                        'title': 'Beat Hip-Hop Commerciale',
                        'description': 'Produzione beat hip-hop moderno per artista emergente, stile trap melodico.',
                        'external_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                        'external_audio_url': 'https://soundcloud.com/example-portfolio/hiphop-beat',
                        'external_image_url': 'https://picsum.photos/400/300?random=3',
                    },
                ]

                created_portfolio = 0
                associates = Associate.objects.all()
                
                for i, associate in enumerate(associates):
                    # Ogni associato ottiene 1-2 elementi portfolio
                    items_to_create = random.randint(1, min(2, len(portfolio_data)))
                    for j in range(items_to_create):
                        if portfolio_data:
                            portfolio_item = portfolio_data.pop(0)
                            PortfolioItem.objects.create(
                                associate=associate,
                                **portfolio_item
                            )
                            created_portfolio += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'📊 Database popolato con successo!\n'
                        f'   🎤 Artisti creati: {created_artists}\n'
                        f'   🔧 Associati creati: {created_associates}\n'
                        f'   🎵 Demo create: {created_demos}\n'
                        f'   💼 Portfolio items: {created_portfolio}\n'
                        f'   🔗 Tutti utilizzano URL esterni (Render-friendly!)\n'
                        f'   📷 Avatar: pravatar.cc (placeholder)\n'
                        f'   🎶 Demo: SoundCloud/YouTube links\n'
                        f'   🖼️ Immagini: Picsum (placeholder)'
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Errore nel popolamento: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))