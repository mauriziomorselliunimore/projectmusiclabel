from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Messaging URLs
    path('', views.inbox, name='inbox'),
    path('conversations/', views.conversations_list, name='conversations'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation'),
    path('send/<int:recipient_id>/', views.send_message, name='send'),
    path('message/<int:pk>/', views.message_detail, name='detail'),
    path('message/<int:pk>/reply/', views.reply_message, name='reply'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
]