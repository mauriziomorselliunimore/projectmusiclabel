from django.contrib import admin
from .admin_site import HealthCheckAdminSite
from artists.models.collaboration import CollaborationProposal
from messaging.models import Message, Conversation, Notification

# Register models
@admin.register(CollaborationProposal)
class CollaborationProposalAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'type', 'budget', 'status', 'created_at')
    list_filter = ('status', 'type', 'mode', 'timeline')
    search_fields = ('sender__username', 'receiver__username', 'description')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'message_type', 'created_at')
    list_filter = ('message_type', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'message')
    date_hierarchy = 'created_at'

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_1', 'participant_2', 'created_at', 'updated_at')
    search_fields = ('participant_1__username', 'participant_2__username')
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'

# Crea una nuova istanza dell'AdminSite personalizzato
admin_site = HealthCheckAdminSite(name='admin')

# Sostituisce l'AdminSite di default con il nostro personalizzato
admin.site = admin_site