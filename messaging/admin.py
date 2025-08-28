from django.contrib import admin
from django.utils.html import format_html
from .models import Message, Notification, Conversation

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'message_type', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Partecipanti', {
            'fields': ('sender', 'recipient')
        }),
        ('Contenuto', {
            'fields': ('message_type', 'subject', 'message')
        }),
        ('Collegamenti', {
            'fields': ('related_booking',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_archived')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read_badge', 'email_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'email_sent', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">✓ Letta</span>')
        return format_html('<span style="color: red;">✗ Non letta</span>')
    is_read_badge.short_description = 'Status Lettura'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifiche segnate come lette.')
    mark_as_read.short_description = "Segna come lette"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifiche segnate come non lette.')
    mark_as_unread.short_description = "Segna come non lette"

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['participant_1', 'participant_2', 'last_message_date', 'created_at']
    search_fields = ['participant_1__username', 'participant_2__username']
    readonly_fields = ['created_at', 'updated_at', 'last_message', 'last_message_date']