from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Inbox e conversazioni
    path('', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation'),
    path('send/<int:user_id>/', views.send_message, name='send'),
    
    # Notifiche
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # API per conteggi (AJAX)
    path('api/unread-counts/', views.get_unread_counts, name='unread_counts'),
]