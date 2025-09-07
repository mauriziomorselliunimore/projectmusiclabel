from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg
import random

from artists.models import Artist
from associates.models import Associate
from reviews.models import Review

def home(request):
    """Vista home page con lista artisti e professionisti"""
    artists = Artist.objects.select_related('user').all()
    associates = Associate.objects.select_related('user').all()
    
    # Mischia artisti e professionisti
    professionals = list(artists) + list(associates)
    random.shuffle(professionals)
    
    # Limita a un massimo di 12 professionisti
    professionals = professionals[:12]
    
    # Prepara i dati per il template con ratings
    professionals_data = []
    for prof in professionals:
        user = prof.user
        avg_rating = None
        review_type = 'associate_to_artist' if isinstance(prof, Artist) else 'artist_to_associate'
        
        # Calcola rating medio
        reviews = Review.objects.filter(reviewed=user, review_type=review_type)
        if reviews.exists():
            avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        # Prepara i dati per il template
        prof_data = {
            'id': prof.id,
            'user': user,
            'name': prof.stage_name if isinstance(prof, Artist) else prof.business_name,
            'type': 'Artista' if isinstance(prof, Artist) else 'Professionista',
            'url': prof.get_absolute_url(),
            'genres': prof.get_genres_list() if isinstance(prof, Artist) else prof.get_specializations_list(),
            'profile_icon': getattr(prof, 'profile_icon', None),
            'profile_icon_color': getattr(prof, 'profile_icon_color', '#ff2e88'),
            'avatar': getattr(prof, 'avatar', None),
            'avg_rating': round(avg_rating, 1) if avg_rating else None
        }
        professionals_data.append(prof_data)
    
    context = {
        'professionals': professionals_data,
        'has_superuser': User.objects.filter(is_superuser=True).exists(),
    }
    
    return render(request, 'core/home.html', context)
