from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Booking, Availability

    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'completed': '#6c757d',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'status'
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) confermati.')
    mark_as_confirmed.short_description = "Conferma booking selezionati"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'{updated} booking(s) completati.')
    mark_as_completed.short_description = "Completa booking selezionati"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.exclude(status='completed').update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) cancellati.')
    mark_as_cancelled.short_description = "Cancella booking selezionati"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'artist__user', 'associate__user'
        )
