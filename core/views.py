from django.shortcuts import render
from django.db.models import Q
from artists.models import Artist
from associates.models import Associate

def home(request):
    """Homepage with search functionality"""
    query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    
    # Get recent artists and associates
    recent_artists = Artist.objects.all()[:6]
    recent_associates = Associate.objects.all()[:6]
    
    # Search functionality
    search_results = []
    if query:
        artists = Artist.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(stage_name__icontains=query) |
            Q(genres__icontains=query)
        )
        associates = Associate.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(skills__icontains=query) |
            Q(specialization__icontains=query)
        )
        search_results = list(artists) + list(associates)
    
    context = {
        'recent_artists': recent_artists,
        'recent_associates': recent_associates,
        'search_results': search_results,
        'search_query': query,
    }
    return render(request, 'core/templates/home.html', context)