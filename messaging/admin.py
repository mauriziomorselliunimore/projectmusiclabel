from django.contrib import admin
from .models import Conversation, Message, Notification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created_at', 'updated_at', 'get_messages_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participant_1__username', 'participant_1__first_name', 'participant_1__last_name',
                     'participant_2__username', 'participant_2__first_name', 'participant_2__last_name']
    readonly_fields = ['created_at', 'updated_at', 'last_message_date']
    raw_id_fields = ['participant_1', 'participant_2', 'last_message']
    
    def get_participants(self, obj):
        return f"{obj.participant_1.get_full_name() or obj.participant_1.username} - {obj.participant_2.get_full_name() or obj.participant_2.username}"
    get_participants.short_description = 'Partecipanti'
    
    def get_messages_count(self, obj):
        return obj.messages.count()
    get_messages_count.short_description = 'Messaggi'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'recipient', 'content_preview', 'created_at', 'is_read']
    list_filter = ['created_at', 'is_read', 'message_type']
    search_fields = ['sender__username', 'recipient__username', 'message', 'subject']
    readonly_fields = ['created_at']
    raw_id_fields = ['conversation', 'sender', 'recipient', 'related_booking']
    
    fieldsets = (
        ('Partecipanti', {
            'fields': ('conversation', 'sender', 'recipient')
        }),
        ('Contenuto', {
            'fields': ('message_type', 'subject', 'message')
        }),
        ('Stati', {
            'fields': ('is_read', 'is_archived')
        }),
        ('Collegamenti', {
            'fields': ('related_booking',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def content_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    content_preview.short_description = 'Anteprima'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} messaggi segnati come letti.")
    mark_as_read.short_description = "Segna come letti"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} messaggi segnati come non letti.")
    mark_as_unread.short_description = "Segna come non letti"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at', 'related_user']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'related_user', 'related_message', 'related_booking']
    
    fieldsets = (
        ('Destinatario', {
            'fields': ('user',)
        }),
        ('Contenuto', {
            'fields': ('notification_type', 'title', 'message', 'action_url')
        }),
        ('Stati', {
            'fields': ('is_read', 'email_sent')
        }),
        ('Collegamenti', {
            'fields': ('related_user', 'related_message', 'related_booking'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'send_email_notifications']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notifiche segnate come lette.")
    mark_as_read.short_description = "Segna come lette"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notifiche segnate come non lette.")
    mark_as_unread.short_description = "Segna come non lette"
    
    def send_email_notifications(self, request, queryset):
        # Placeholder per invio email notifiche
        count = queryset.filter(email_sent=False).count()
        queryset.update(email_sent=True)
        self.message_user(request, f"{count} notifiche email inviate.")
    send_email_notifications.short_description = "Invia notifiche email"