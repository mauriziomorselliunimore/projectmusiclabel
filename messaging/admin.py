from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Message, Notification, Conversation

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'sender_link', 'recipient_link', 'subject_truncated', 
        'message_type', 'is_read_badge', 'created_at'
    ]
    list_filter = [
        'message_type', 'is_read', 'is_archived', 'created_at'
    ]
    search_fields = [
        'sender__username', 'sender__first_name', 'sender__last_name',
        'recipient__username', 'recipient__first_name', 'recipient__last_name',
        'subject', 'message'
    ]
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
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
    
    actions = ['mark_as_read', 'mark_as_unread', 'archive_messages']
    
    def sender_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.sender.pk])
        return format_html('<a href="{}">{}</a>', url, obj.sender.username)
    sender_link.short_description = "Mittente"
    sender_link.admin_order_field = 'sender__username'
    
    def recipient_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.recipient.pk])
        return format_html('<a href="{}">{}</a>', url, obj.recipient.username)
    recipient_link.short_description = "Destinatario"
    recipient_link.admin_order_field = 'recipient__username'
    
    def subject_truncated(self, obj):
        if len(obj.subject) > 50:
            return obj.subject[:47] + "..."
        return obj.subject
    subject_truncated.short_description = "Oggetto"
    subject_truncated.admin_order_field = 'subject'
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">●</span> Letto')
        return format_html('<span style="color: orange;">●</span> Non letto')
    is_read_badge.short_description = "Status"
    is_read_badge.admin_order_field = 'is_read'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messaggio/i segnati come letti.')
    mark_as_read.short_description = "Segna come letti"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} messaggio/i segnati come non letti.')
    mark_as_unread.short_description = "Segna come non letti"
    
    def archive_messages(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, f'{updated} messaggio/i archiviati.')
    archive_messages.short_description = "Archivia messaggi"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'recipient', 'related_booking')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_link', 'notification_type', 'title_truncated', 
        'is_read_badge', 'email_sent_badge', 'created_at'
    ]
    list_filter = [
        'notification_type', 'is_read', 'email_sent', 'created_at'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'title', 'message'
    ]
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Destinatario', {
            'fields': ('user',)
        }),
        ('Contenuto', {
            'fields': ('notification_type', 'title', 'message', 'action_url')
        }),
        ('Collegamenti', {
            'fields': ('related_booking', 'related_message', 'related_user'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'email_sent')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'send_email_notifications']
    
    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utente"
    user_link.admin_order_field = 'user__username'
    
    def title_truncated(self, obj):
        if len(obj.title) > 40:
            return obj.title[:37] + "..."
        return obj.title
    title_truncated.short_description = "Titolo"
    title_truncated.admin_order_field = 'title'
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">●</span> Letta')
        return format_html('<span style="color: orange;">●</span> Non letta')
    is_read_badge.short_description = "Lettura"
    is_read_badge.admin_order_field = 'is_read'
    
    def email_sent_badge(self, obj):
        if obj.email_sent:
            return format_html('<span style="color: blue;">●</span> Inviata')
        return format_html('<span style="color: gray;">●</span> Non inviata')
    email_sent_badge.short_description = "Email"
    email_sent_badge.admin_order_field = 'email_sent'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifica/che segnate come lette.')
    mark_as_read.short_description = "Segna come lette"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifica/che segnate come non lette.')
    mark_as_unread.short_description = "Segna come non lette"
    
    def send_email_notifications(self, request, queryset):
        # Qui implementeresti l'invio email
        count = queryset.filter(email_sent=False).count()
        queryset.update(email_sent=True)
        self.message_user(request, f'{count} email di notifica inviate.')
    send_email_notifications.short_description = "Invia email notifiche"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'related_booking', 'related_message', 'related_user'
        )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'participant_1_link', 'participant_2_link', 
        'messages_count', 'last_message_date', 'created_at'
    ]
    list_filter = ['created_at', 'last_message_date']
    search_fields = [
        'participant_1__username', 'participant_1__first_name', 'participant_1__last_name',
        'participant_2__username', 'participant_2__first_name', 'participant_2__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'last_message', 'last_message_date']
    
    fieldsets = (
        ('Partecipanti', {
            'fields': ('participant_1', 'participant_2')
        }),
        ('Cache', {
            'fields': ('last_message', 'last_message_date'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def participant_1_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.participant_1.pk])
        return format_html('<a href="{}">{}</a>', url, obj.participant_1.username)
    participant_1_link.short_description = "Partecipante 1"
    participant_1_link.admin_order_field = 'participant_1__username'
    
    def participant_2_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.participant_2.pk])
        return format_html('<a href="{}">{}</a>', url, obj.participant_2.username)
    participant_2_link.short_description = "Partecipante 2"
    participant_2_link.admin_order_field = 'participant_2__username'
    
    def messages_count(self, obj):
        return obj.get_messages().count()
    messages_count.short_description = "N° Messaggi"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'participant_1', 'participant_2', 'last_message'
        )