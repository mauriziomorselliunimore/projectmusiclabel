from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from accounts.models import Profile
import random
import os

def auto_populate_if_needed():
    """Auto-popola il database se è vuoto e AUTO_POPULATE=True"""
    if not os.environ.get('AUTO_POPULATE'):
        return
    
    # Se non ci sono artisti, popola il database
    if not Artist.objects.exists():
        try:
            # Crea superuser se non esiste
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@mylabel.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='MyLabel'
                )
                print("✅ Admin creato!")
            
            # Popola il database
            populate_database_programmatically()
            print("✅ Database popolato!")
            
        except Exception as e:
            print(f"⚠️ Errore auto-popolamento: {e}")

def populate_database_programmatically():
    """Popola il database programmaticamente"""
    with transaction.atomic():
        # Dati di esempio compatti per Render
        artists_data = [
            {
                'username': 'marco_blues', 'email': 'marco@example.com',
                'first_name': 'Marco', 'last_name': 'Rossi',
                'stage_name': 'Blues Marco', 'genres': 'Blues, Rock, Jazz',
                'bio': 'Chitarrista blues con esperienza live.', 'location': 'Roma, Italia',
                'phone': '+39 333 111 2222',
            },
            {
                'username': 'sofia_pop', 'email': 'sofia@example.com',
                'first_name': 'Sofia', 'last_name': 'Bianchi',
                'stage_name': 'Sofia B', 'genres': 'Pop, R&B, Soul',
                'bio': 'Cantante pop emergente, X Factor 2023.', 'location': 'Milano, Italia',
                'phone': '+39 333 333 4444',
            },
            {
                'username': 'dj_elektro', 'email': 'alessandro@example.com',
                'first_name': 'Alessandro', 'last_name': 'Verdi',
                'stage_name': 'DJ Elektro', 'genres': 'Electronic, House, Techno',
                'bio': 'Producer elettronico e DJ resident.', 'location': 'Napoli, Italia',
                'phone': '+39 333 555 6666',
            }
        ]

        associates_data = [
            {
                'username': 'luca_sound', 'email': 'luca@example.com',
                'first_name': 'Luca', 'last_name': 'Ferrari',
                'specialization': 'Sound Engineer', 'hourly_rate': 45.00,
                'skills': 'Pro Tools, Logic Pro, Mixing, Mastering',
                'experience_level': 'professional', 'years_experience': 12,
                'bio': 'Fonico con 10+ anni di esperienza.', 'location': 'Roma, Italia',
            },
            {
                'username': 'anna_producer', 'email': 'anna@example.com',
                'first_name': 'Anna', 'last_name': 'Romano',
                'specialization': 'Music Producer', 'hourly_rate': 35.00,
                'skills': 'Ableton Live, Composizione, Beat Making',
                'experience_level': 'advanced', 'years_experience': 7,
                'bio': 'Producer specializzata pop e hip-hop.', 'location': 'Milano, Italia',
            }
        ]

        # Crea artisti
        for data in artists_data:
            user_fields = ['username', 'email', 'first_name', 'last_name']
            user_data = {k: data[k] for k in user_fields}
            artist_data = {k: v for k, v in data.items() if k not in user_fields}

            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            if created:
                user.set_password('password123')
                user.save()
                Profile.objects.create(user=user, user_type='artist')
                Artist.objects.create(user=user, **artist_data)

        # Crea associati
        for data in associates_data:
            user_fields = ['username', 'email', 'first_name', 'last_name']
            user_data = {k: data[k] for k in user_fields}
            associate_data = {k: v for k, v in data.items() if k not in user_fields}

            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            if created:
                user.set_password('password123')
                user.save()
                Profile.objects.create(user=user, user_type='associate')
                Associate.objects.create(user=user, **associate_data)

        # Crea demo rapide
        demo_data = [
            ('Midnight Blues', 'blues', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            ('Electric Dreams', 'electronic', 'https://soundcloud.com/example/electric-dreams'),
            ('Summer Vibes', 'pop', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            ('Rock Revolution', 'rock', 'https://soundcloud.com/example/rock-revolution'),
            ('Soul Connection', 'r&b', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            ('Urban Beat', 'hip-hop', 'https://soundcloud.com/example/urban-beat'),
        ]

        artists = Artist.objects.all()[:3]
        for i, artist in enumerate(artists):
            for j in range(2):  # 2 demo per artista
                demo_index = i * 2 + j
                if demo_index < len(demo_data):
                    title, genre, audio_url = demo_data[demo_index]
                    Demo.objects.get_or_create(
                        artist=artist,
                        title=title,
                        defaults={
                            'genre': genre,
                            'description': f'Demo {title} by {artist.stage_name}',
                            'external_audio_url': audio_url,
                            'duration': f"{random.randint(2,4)}:{random.randint(10,59):02d}",
                            'is_public': True,
                        }
                    )

def home(request):
    """Homepage con statistiche e gestione Render-friendly"""
    
    # Auto-popola se necessario (solo al primo caricamento)
    auto_populate_if_needed()
    
    stats = {
        'total_artists': Artist.objects.filter(is_active=True).count(),
        'total_associates': Associate.objects.filter(is_active=True).count(),
        'total_demos': Demo.objects.filter(is_public=True).count(),
        'latest_artists': Artist.objects.filter(is_active=True).order_by('-created_at')[:3],
        'latest_associates': Associate.objects.filter(is_active=True, is_available=True).order_by('-created_at')[:3],
        'is_render': bool(os.environ.get('RENDER')),
        'has_superuser': User.objects.filter(is_superuser=True).exists(),
    }
    return render(request, 'home.html', stats)

@user_passes_test(lambda u: u.is_superuser)
def populate_database(request):
    """Popola database - versione ottimizzata per Render free"""
    try:
        # Check se già popolato
        if Artist.objects.exists() and Associate.objects.exists():
            messages.info(request, '📊 Database già popolato!')
            return redirect('core:home')

        populate_database_programmatically()
        
        messages.success(
            request,
            f'✅ Database popolato! Artisti: {Artist.objects.count()}, '
            f'Associati: {Associate.objects.count()}, Demo: {Demo.objects.count()}'
        )

    except Exception as e:
        messages.error(request, f'❌ Errore popolamento: {str(e)}')

    return redirect('core:home')

@user_passes_test(lambda u: u.is_superuser)
def clear_database(request):
    """Svuota database - sicuro per Render"""
    try:
        with transaction.atomic():
            # Elimina solo dati non-admin
            Demo.objects.all().delete()
            PortfolioItem.objects.all().delete()
            Artist.objects.all().delete()
            Associate.objects.all().delete()
            
            # Elimina profili non-admin
            Profile.objects.exclude(user__is_superuser=True).delete()
            
            # Elimina utenti non-admin
            User.objects.filter(is_superuser=False, is_staff=False).delete()

        messages.success(request, '🗑️ Database svuotato (admin preservato)!')
    except Exception as e:
        messages.error(request, f'❌ Errore: {str(e)}')

    return redirect('core:home')

def create_superuser_render(request):
    """Crea superuser via web (solo se non esiste) - per Render free"""
    if request.method == 'POST' and not User.objects.filter(is_superuser=True).exists():
        try:
            User.objects.create_superuser(
                username='admin',
                email='admin@mylabel.com', 
                password='admin123',
                first_name='Admin',
                last_name='MyLabel'
            )
            messages.success(
                request, 
                '👨‍💼 Superuser creato! Username: admin, Password: admin123 (CAMBIALA SUBITO!)'
            )
        except Exception as e:
            messages.error(request, f'❌ Errore creazione admin: {str(e)}')
    
    return redirect('core:home')

def render_status(request):
    """API endpoint per stato del sistema - utile per debugging"""
    return JsonResponse({
        'render_detected': bool(os.environ.get('RENDER')),
        'debug_mode': os.environ.get('DEBUG', 'False').lower() == 'true',
        'has_superuser': User.objects.filter(is_superuser=True).exists(),
        'artists_count': Artist.objects.count(),
        'associates_count': Associate.objects.count(),
        'demos_count': Demo.objects.count(),
        'auto_populate_enabled': bool(os.environ.get('AUTO_POPULATE')),
        'database_engine': 'postgresql' if 'postgres' in str(type(User.objects.all()._db)) else 'sqlite',
    })