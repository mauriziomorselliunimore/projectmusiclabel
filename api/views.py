from rest_framework import generics, filters, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.contrib.auth.models import User

from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from booking.models import Booking
from messaging.models import Message, Notification, Conversation
from .serializers import *

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

# Artists API Views
class ArtistListAPIView(generics.ListAPIView):
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location']
    search_fields = ['stage_name', 'genres', 'bio', 'user__first_name', 'user__last_name']
    ordering_fields = ['stage_name', 'created_at']
    ordering = ['-created_at']

class ArtistDetailAPIView(generics.RetrieveAPIView):
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistDetailSerializer

# Associates API Views
class AssociateListAPIView(generics.ListAPIView):
    queryset = Associate.objects.filter(is_active=True, is_available=True)
    serializer_class = AssociateListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'experience_level', 'location']
    search_fields = ['specialization', 'skills', 'bio', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'created_at', 'hourly_rate']
    ordering = ['-created_at']

class AssociateDetailAPIView(generics.RetrieveAPIView):
    queryset = Associate.objects.filter(is_active=True)
    serializer_class = AssociateDetailSerializer

# Demos API Views
class DemoListAPIView(generics.ListAPIView):
    serializer_class = DemoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'artist']
    search_fields = ['title', 'description', 'artist__stage_name']
    ordering_fields = ['title', 'uploaded_at']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        return Demo.objects.filter(is_public=True).select_related('artist')

class DemoDetailAPIView(generics.RetrieveAPIView):
    queryset = Demo.objects.filter(is_public=True)
    serializer_class = DemoSerializer

# Bookings API Views (Authenticated only)
class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'booking_type']
    ordering_fields = ['session_date', 'created_at']
    ordering = ['-session_date']
    
    def get_queryset(self):
        # Solo booking dell'utente corrente
        if hasattr(self.request.user, 'artist'):
            return Booking.objects.filter(artist=self.request.user.artist)
        elif hasattr(self.request.user, 'associate'):
            return Booking.objects.filter(associate=self.request.user.associate)
        return Booking.objects.none()

class MyBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        if hasattr(self.request.user, 'artist'):
            return Booking.objects.filter(artist=self.request.user.artist).order_by('-session_date')
        elif hasattr(self.request.user, 'associate'):
            return Booking.objects.filter(associate=self.request.user.associate).order_by('-session_date')
        return Booking.objects.none()

class BookingDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'artist'):
            return Booking.objects.filter(artist=self.request.user.artist)
        elif hasattr(self.request.user, 'associate'):
            return Booking.objects.filter(associate=self.request.user.associate)
        return Booking.objects.none()

# Messages API Views (Authenticated only)
class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).select_related('sender', 'recipient')

class MessageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        )

class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    ordering = ['-updated_at']
    
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(participant_1=self.request.user) | Q(participant_2=self.request.user)
        ).select_related('participant_1', 'participant_2', 'last_message')

# Notifications API Views (Authenticated only)
class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notifications_read_api(request):
    """API endpoint per segnare notifiche come lette"""
    try:
        notification_ids = request.data.get('notification_ids', [])
        
        if notification_ids:
            # Segna solo le notifiche specificate
            updated = Notification.objects.filter(
                user=request.user,
                id__in=notification_ids,
                is_read=False
            ).update(is_read=True)
        else:
            # Segna tutte le notifiche come lette
            updated = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).update(is_read=True)
        
        return Response({
            'success': True,
            'updated': updated,
            'message': f'{updated} notifiche segnate come lette.'
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Search API
class GlobalSearchAPIView(generics.ListAPIView):
    serializer_class = GlobalSearchSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []
        
        # Cerca in artisti, associati e demo
        results = []
        
        # Artisti
        artists = Artist.objects.filter(
            Q(stage_name__icontains=query) |
            Q(genres__icontains=query) |
            Q(bio__icontains=query),
            is_active=True
        )[:5]
        
        for artist in artists:
            results.append({
                'type': 'artist',
                'id': artist.id,
                'title': artist.stage_name,
                'subtitle': artist.genres,
                'url': artist.get_absolute_url(),
                'avatar': artist.user.profile.get_avatar_url(),
            })
        
        # Associati
        associates = Associate.objects.filter(
            Q(specialization__icontains=query) |
            Q(skills__icontains=query) |
            Q(bio__icontains=query),
            is_active=True
        )[:5]
        
        for associate in associates:
            results.append({
                'type': 'associate',
                'id': associate.id,
                'title': associate.user.get_full_name(),
                'subtitle': associate.specialization,
                'url': associate.get_absolute_url(),
                'avatar': associate.user.profile.get_avatar_url(),
            })
        
        # Demo
        demos = Demo.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_public=True
        ).select_related('artist')[:5]
        
        for demo in demos:
            results.append({
                'type': 'demo',
                'id': demo.id,
                'title': demo.title,
                'subtitle': f"{demo.artist.stage_name} - {demo.get_genre_display()}",
                'url': demo.external_audio_url or '#',
                'avatar': demo.artist.user.profile.get_avatar_url(),
            })
        
        return results

# Stats API
@api_view(['GET'])
def api_stats(request):
    """API endpoint per statistiche globali della piattaforma"""
    try:
        stats = {
            'platform': {
                'total_artists': Artist.objects.filter(is_active=True).count(),
                'total_associates': Associate.objects.filter(is_active=True).count(),
                'total_demos': Demo.objects.filter(is_public=True).count(),
                'total_bookings': Booking.objects.count(),
                'total_users': User.objects.filter(is_active=True).count(),
            },
            'recent_activity': {
                'recent_artists': ArtistListSerializer(
                    Artist.objects.filter(is_active=True).order_by('-created_at')[:5], 
                    many=True
                ).data,
                'recent_demos': DemoSerializer(
                    Demo.objects.filter(is_public=True).order_by('-uploaded_at')[:5],
                    many=True
                ).data,
            },
            'popular_genres': list(
                Demo.objects.filter(is_public=True)
                .values('genre')
                .annotate(count=Count('genre'))
                .order_by('-count')[:10]
            ),
        }
        
        # Stats specifiche per utente autenticato
        if request.user.is_authenticated:
            user_stats = {}
            
            if hasattr(request.user, 'artist'):
                user_stats['artist'] = {
                    'demos_count': request.user.artist.demos.filter(is_public=True).count(),
                    'bookings_count': request.user.artist.bookings.count(),
                }
            
            if hasattr(request.user, 'associate'):
                user_stats['associate'] = {
                    'bookings_count': request.user.associate.bookings.count(),
                    'portfolio_count': request.user.associate.portfolio_items.count(),
                }
            
            user_stats['messaging'] = {
                'unread_messages': Message.objects.filter(recipient=request.user, is_read=False).count(),
                'unread_notifications': Notification.objects.filter(user=request.user, is_read=False).count(),
            }
            
            stats['user'] = user_stats
        
        return Response(stats)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)