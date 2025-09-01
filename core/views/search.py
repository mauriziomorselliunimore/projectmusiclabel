from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from ..models import Artist, Demo
from associates.models import Associate

@login_required
def advanced_search(request):
    """Vista per la ricerca avanzata di artisti e associati"""
    # Inizializza QuerySets vuoti
    artists = Artist.objects.filter(is_active=True)
    associates = Associate.objects.filter(is_active=True)
    
    # Parametri di ricerca
    search_query = request.GET.get('q', '').strip()
    user_type = request.GET.get('type', 'all')  # 'artists', 'associates', 'all'
    genre = request.GET.get('genre', '')
    skills = request.GET.getlist('skills', [])
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('availability')  # 'weekday', 'weekend', 'any'
    
    # Applica filtri di ricerca
    if search_query:
        artists = artists.filter(
            Q(stage_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(genres__icontains=search_query)
        )
        associates = associates.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )
    
    # Filtro per genere musicale (solo artisti)
    if genre and user_type != 'associates':
        artists = artists.filter(genres__icontains=genre)
    
    # Filtro per competenze (solo associati)
    if skills and user_type != 'artists':
        for skill in skills:
            associates = associates.filter(skills__icontains=skill)
    
    # Filtro per prezzo (solo associati)
    if user_type != 'artists':
        if min_price:
            associates = associates.filter(hourly_rate__gte=float(min_price))
        if max_price:
            associates = associates.filter(hourly_rate__lte=float(max_price))
    
    # Filtro per disponibilità (solo associati)
    if availability and user_type != 'artists':
        if availability == 'weekday':
            associates = associates.filter(availability_slots__weekday__in=[0,1,2,3,4])
        elif availability == 'weekend':
            associates = associates.filter(availability_slots__weekday__in=[5,6])
    
    # Filtra per tipo utente
    if user_type == 'artists':
        associates = Associate.objects.none()
    elif user_type == 'associates':
        artists = Artist.objects.none()
    
    # Recupera le demo per gli artisti
    artists = artists.prefetch_related('demos')
    
    context = {
        'artists': artists.distinct(),
        'associates': associates.distinct(),
        'search_query': search_query,
        'user_type': user_type,
        'genre': genre,
        'skills': skills,
        'min_price': min_price,
        'max_price': max_price,
        'availability': availability,
        'genres': Artist.GENRES,  # Per il dropdown dei generi
        'skill_choices': Associate.SKILLS,  # Per i checkbox delle competenze
    }
    
    return render(request, 'search/advanced_search.html', context)
