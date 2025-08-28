from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

# Router per ViewSets (se ne aggiungi in futuro)
router = DefaultRouter()

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Artists API
    path('artists/', views.ArtistListAPIView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', views.ArtistDetailAPIView.as_view(), name='artist-detail'),
    
    # Associates API  
    path('associates/', views.AssociateListAPIView.as_view(), name='associate-list'),
    path('associates/<int:pk>/', views.AssociateDetailAPIView.as_view(), name='associate-detail'),
    
    # Demos API
    path('demos/', views.DemoListAPIView.as_view(), name='demo-list'),
    path('demos/<int:pk>/', views.DemoDetailAPIView.as_view(), name='demo-detail'),
    
    # Bookings API (authenticated users only)
    path('my-bookings/', views.MyBookingsAPIView.as_view(), name='my-bookings'),
    path('bookings/', views.BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailAPIView.as_view(), name='booking-detail'),
    
    # Messages API (authenticated users only)
    path('messages/', views.MessageListAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetailAPIView.as_view(), name='message-detail'),
    path('conversations/', views.ConversationListAPIView.as_view(), name='conversation-list'),
    
    # Notifications API (authenticated users only)
    path('notifications/', views.NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/mark-read/', views.mark_notifications_read_api, name='mark-notifications-read'),
    
    # Stats and search
    path('stats/', views.api_stats, name='stats'),
    path('search/', views.GlobalSearchAPIView.as_view(), name='search'),
    
    # Auth endpoints
    path('auth/', include('rest_framework.urls')),
]
