from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from artists.models import Artist
from associates.models import Associate
from django.contrib.auth import get_user_model

def home(request):
    """Homepage con ricerca e ultimi inserimenti"""
    query = request.GET.get('search', '').strip()
    genre_filter = request.GET.get('genre', '').strip()

    # Ultimi 6 artisti e associati
    recent_artists = Artist.objects.all()[:6]
    recent_associates = Associate.objects.all()[:6]

    search_results = []
    if query or genre_filter:
        artists = Artist.objects.all()
        associates = Associate.objects.all()

        # Filtra per testo
        if query:
            artists = artists.filter(
                Q(user__first_name__icontains=query) |
                Q(stage_name__icontains=query) |
                Q(genres__icontains=query)
            )
            associates = associates.filter(
                Q(user__first_name__icontains=query) |
                Q(skills__icontains=query) |
                Q(specialization__icontains=query)
            )

        # Filtra per genere, se presente
        if genre_filter:
            artists = artists.filter(genres__icontains=genre_filter)
            associates = associates.filter(skills__icontains=genre_filter)

        search_results = list(artists) + list(associates)

    context = {
        'recent_artists': recent_artists,
        'recent_associates': recent_associates,
        'search_results': search_results,
        'search_query': query,
        'genre_filter': genre_filter,
    }
    return render(request, 'home.html', context)

def profilo(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'profilo.html', {'user': user})
