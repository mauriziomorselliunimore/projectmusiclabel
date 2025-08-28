# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from artists.models import Artist, Demo
from associates.models import Associate, PortfolioItem
from booking.models import Booking
from messaging.models import Message, Notification, Conversation

class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer base per User con info essenziali"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'avatar_url']
    
    def get_avatar_url(self, obj):
        return obj.profile.get_avatar_url() if hasattr(obj, 'profile') else None

# Artists Serializers
class ArtistListSerializer(serializers.ModelSerializer):
    """Serializer per lista artisti"""
    user = UserBasicSerializer(read_only=True)
    demos_count = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    genres_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'stage_name', 'genres', 'genres_list', 'location', 
            'user', 'avatar_url', 'demos_count', 'created_at'
        ]
    
    def get_demos_count(self, obj):
        return obj.demos.filter(is_public=True).count()
    
    def get_avatar_url(self, obj):
        return obj.user.profile.get_avatar_url()
    
    def get_genres_list(self, obj):
        return obj.get_genres_list()

class ArtistDetailSerializer(ArtistListSerializer):
    """Serializer dettagliato per singolo artista"""
    demos = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    
    class Meta(ArtistListSerializer.Meta):
        fields = ArtistListSerializer.Meta.fields + [
            'bio', 'phone', 'demos', 'social_links', 
            'spotify_url', 'youtube_url', 'soundcloud_url', 'instagram_url'
        ]
    
    def get_demos(self, obj):
        demos = obj.demos.filter(is_public=True).order_by('-uploaded_at')[:10]
        return DemoSerializer(demos, many=True).data
    
    def get_social_links(self, obj):
        return {
            'spotify': obj.spotify_url,
            'youtube': obj.youtube_url,
            'soundcloud': obj.soundcloud_url,
            'instagram': obj.instagram_url,
        }

# Associates Serializers
class AssociateListSerializer(serializers.ModelSerializer):
    """Serializer per lista associati"""
    user = UserBasicSerializer(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    skills_list = serializers.SerializerMethodField()
    rate_display = serializers.CharField(source='get_rate_display', read_only=True)
    portfolio_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Associate
        fields = [
            'id', 'specialization', 'skills', 'skills_list', 'experience_level',
            'hourly_rate', 'rate_display', 'location', 'is_available',
            'user', 'avatar_url', 'portfolio_count', 'created_at'
        ]
    
    def get_avatar_url(self, obj):
        return obj.user.profile.get_avatar_url()
    
    def get_skills_list(self, obj):
        return obj.get_skills_list()
    
    def get_portfolio_count(self, obj):
        return obj.portfolio_items.count()

class AssociateDetailSerializer(AssociateListSerializer):
    """Serializer dettagliato per singolo associato"""
    portfolio_items = serializers.SerializerMethodField()
    
    class Meta(AssociateListSerializer.Meta):
        fields = AssociateListSerializer.Meta.fields + [
            'bio', 'phone', 'website', 'portfolio_description', 
            'years_experience', 'availability', 'portfolio_items'
        ]
    
    def get_portfolio_items(self, obj):
        items = obj.portfolio_items.order_by('-created_at')[:10]
        return PortfolioItemSerializer(items, many=True).data

class PortfolioItemSerializer(serializers.ModelSerializer):
    """Serializer per elementi portfolio"""
    associate_name = serializers.CharField(source='associate.user.get_full_name', read_only=True)
    primary_url = serializers.CharField(source='get_primary_url', read_only=True)
    platform = serializers.CharField(source='get_platform', read_only=True)
    
    class Meta:
        model = PortfolioItem
        fields = [
            'id', 'title', 'description', 'external_image_url', 
            'external_audio_url', 'external_url', 'primary_url', 
            'platform', 'associate_name', 'created_at'
        ]

# Demos Serializers
class DemoSerializer(serializers.ModelSerializer):
    """Serializer per demo musicali"""
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    artist_id = serializers.IntegerField(source='artist.id', read_only=True)
    platform = serializers.SerializerMethodField()
    artist_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Demo
        fields = [
            'id', 'title', 'genre', 'description', 'duration', 
            'external_audio_url', 'platform', 'artist_name', 
            'artist_id', 'artist_avatar', 'uploaded_at', 'is_public'
        ]
    
    def get_platform(self, obj):
        return obj.get_platform()
    
    def get_artist_avatar(self, obj):
        return obj.artist.user.profile.get_avatar_url()

# Bookings Serializers
class BookingSerializer(serializers.ModelSerializer):
    """Serializer per prenotazioni"""
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    artist_id = serializers.IntegerField(source='artist.id', read_only=True)
    associate_name = serializers.CharField(source='associate.user.get_full_name', read_only=True)
    associate_id = serializers.IntegerField(source='associate.id', read_only=True)
    can_modify = serializers.SerializerMethodField()
    is_upcoming = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'artist_name', 'artist_id', 'associate_name', 'associate_id',
            'booking_type', 'booking_type_display', 'session_date', 'duration_hours', 
            'location', 'notes', 'status', 'status_display', 'total_cost',
            'can_modify', 'is_upcoming', 'created_at', 'updated_at'
        ]
    
    def get_can_modify(self, obj):
        return obj.status == 'pending' and obj.is_upcoming

# Messages Serializers
class MessageSerializer(serializers.ModelSerializer):
    """Serializer per messaggi"""
    sender = UserBasicSerializer(read_only=True)
    recipient = UserBasicSerializer(read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    is_recent = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'message_type', 'message_type_display',
            'subject', 'message', 'is_read', 'is_archived', 'is_recent',
            'created_at'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer per conversazioni"""
    participant_1 = UserBasicSerializer(read_only=True)
    participant_2 = UserBasicSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participant_1', 'participant_2', 'last_message',
            'last_message_date', 'unread_count', 'created_at', 'updated_at'
        ]
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.unread_count_for_user(request.user)
        return 0

# Notifications Serializers
class NotificationSerializer(serializers.ModelSerializer):
    """Serializer per notifiche"""
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    icon_class = serializers.CharField(read_only=True)
    color_class = serializers.CharField(read_only=True)
    is_recent = serializers.BooleanField(read_only=True)
    related_user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'notification_type_display',
            'title', 'message', 'action_url', 'icon_class', 'color_class',
            'is_read', 'email_sent', 'is_recent', 'related_user', 'created_at'
        ]

# Search Serializer
class GlobalSearchSerializer(serializers.Serializer):
    """Serializer per risultati di ricerca globale"""
    type = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    url = serializers.URLField()
    avatar = serializers.URLField()