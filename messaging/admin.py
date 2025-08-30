from django.contrib import admin
from .models import Conversation, Message, Notification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created_at', 'updated_at', 'get_messages_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_participants(self, obj):
        return " - ".join([p.get_full_name() or p.username for p in obj.participants.all()])
    get_participants.short_description = 'Partecipanti'
    
    def get_messages_count(self, obj):
        return obj.messages.count()
    get_messages_count.short_description = 'Messaggi'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'get_recipient', 'content_preview', 'sent_at', 'is_read']
    list_filter = ['sent_at', 'is_read']
    search_fields = ['sender__username', 'content', 'conversation__participants__username']
    readonly_fields = ['sent_at']
    raw_id_fields = ['conversation', 'sender']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Anteprima'
    
    def get_recipient(self, obj):
        other_user = obj.conversation.get_other_participant(obj.sender)
        return other_user.get_full_name() or other_user.username if other_user else "N/A"
    get_recipient.short_description = 'Destinatario'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at', 'related_user']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'related_user']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notifiche segnate come lette.")
    mark_as_read.short_description = "Segna come lette"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notifiche segnate come non lette.")
    mark_as_unread.short_description = "Segna come non lette"