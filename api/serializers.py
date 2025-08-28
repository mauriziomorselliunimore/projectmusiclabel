# api/serializers.py
from rest_framework import serializers
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from booking.models import Booking

class ArtistListSerializer(serializers.ModelSerializer):
    demos_count = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    genres_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = ['id', 'stage_name', 'genres_list', 'location', 'avatar_url', 'demos_count']
    
    def get_demos_count(self, obj):
        return obj.demos.filter(is_public=True).count()
    
    def get_avatar_url(self, obj):
        return obj.user.profile.get_avatar_url()
    
    def get_genres_list(self, obj):
        return obj.get_genres_list()

class ArtistDetailSerializer(ArtistListSerializer):
    demos = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    
    class Meta(ArtistListSerializer.Meta):
        fields = ArtistListSerializer.Meta.fields + [
            'bio', 'phone', 'demos', 'social_links', 'created_at'
        ]
    
    def get_demos(self, obj):
        demos = obj.demos.filter(is_public=True)[:5]
        return DemoSerializer(demos, many=True).data
    
    def get_social_links(self, obj):
        return {
            'spotify': obj.spotify_url,
            'youtube': obj.youtube_url,
            'soundcloud': obj.soundcloud_url,
            'instagram': obj.instagram_url,
        }

class DemoSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    platform = serializers.SerializerMethodField()
    
    class Meta:
        model = Demo
        fields = ['id', 'title', 'genre', 'description', 'duration', 
                 'external_audio_url', 'platform', 'artist_name', 'uploaded_at']
    
    def get_platform(self, obj):
        return obj.get_platform()

class BookingSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    associate_name = serializers.CharField(source='associate.user.get_full_name', read_only=True)
    can_modify = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'artist_name', 'associate_name', 'booking_type', 
                 'session_date', 'duration_hours', 'location', 'status', 
                 'total_cost', 'can_modify', 'created_at']
    
    def get_can_modify(self, obj):
        return obj.status == 'pending' and obj.is_upcoming

# api/views.py
from rest_framework import generics, filters, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArtistListAPIView(generics.ListAPIView):
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location']
    search_fields = ['stage_name', 'genres', 'bio']
    ordering_fields = ['stage_name', 'created_at']
    ordering = ['-created_at']

class ArtistDetailAPIView(generics.RetrieveAPIView):
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistDetailSerializer

class DemoListAPIView(generics.ListAPIView):
    serializer_class = DemoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre', 'artist']
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        return Demo.objects.filter(is_public=True).select_related('artist')

class MyBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        if hasattr(self.request.user, 'artist'):
            return Booking.objects.filter(artist=self.request.user.artist)
        elif hasattr(self.request.user, 'associate'):
            return Booking.objects.filter(associate=self.request.user.associate)
        return Booking.objects.none()

@api_view(['GET'])
def api_stats(request):
    """API endpoint per statistiche globali"""
    return Response({
        'total_artists': Artist.objects.filter(is_active=True).count(),
        'total_associates': Associate.objects.filter(is_active=True).count(),
        'total_demos': Demo.objects.filter(is_public=True).count(),
        'total_bookings': Booking.objects.count(),
        'recent_artists': ArtistListSerializer(
            Artist.objects.filter(is_active=True).order_by('-created_at')[:5], 
            many=True
        ).data
    })

# api/urls.py
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Artists
    path('artists/', views.ArtistListAPIView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', views.ArtistDetailAPIView.as_view(), name='artist-detail'),
    
    # Demos
    path('demos/', views.DemoListAPIView.as_view(), name='demo-list'),
    
    # Bookings
    path('my-bookings/', views.MyBookingsAPIView.as_view(), name='my-bookings'),
    
    # Stats
    path('stats/', views.api_stats, name='stats'),
]