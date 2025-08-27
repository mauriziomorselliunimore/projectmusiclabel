from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Booking, Availability

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'artist_link', 'associate_link', 'session_date', 
        'duration_hours', 'booking_type', 'status_badge', 'total_cost'
    ]
    list_filter = [
        'status', 'booking_type', 'session_date', 'created_at'
    ]
    search_fields = [
        'artist__stage_name', 'artist__user__first_name', 'artist__user__last_name',
        'associate__user__first_name', 'associate__user__last_name', 'associate__specialization'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_cost']
    date_hierarchy = 'session_date'
    
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('artist', 'associate', 'booking_type', 'status')
        }),
        ('Dettagli Sessione', {
            'fields': ('session_date', 'duration_hours', 'location', 'notes', 'special_requirements')
        }),
        ('Costi', {
            'fields': ('total_cost',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def artist_link(self, obj):
        url = reverse("admin:artists_artist_change", args=[obj.artist.pk])
        return format_html('<a href="{}">{}</a>', url, obj.artist.stage_name)
    artist_link.short_description = "Artista"
    artist_link.admin_order_field = 'artist__stage_name'
    
    def associate_link(self, obj):
        url = reverse("admin:associates_associate_change", args=[obj.associate.pk])
        return format_html('<a href="{}">{}</a>', url, obj.associate.user.get_full_name())
    associate_link.short_description = "Associato"
    associate_link.admin_order_field = 'associate__user__last_name'
    
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

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        'associate_name', 'day_display', 'time_range', 
        'is_recurring', 'specific_date', 'is_active'
    ]
    list_filter = [
        'day_of_week', 'is_recurring', 'is_active', 'created_at'
    ]
    search_fields = [
        'associate__user__first_name', 'associate__user__last_name',
        'associate__specialization'
    ]
    
    fieldsets = (
        ('Associato', {
            'fields': ('associate',)
        }),
        ('Disponibilità', {
            'fields': ('day_of_week', 'start_time', 'end_time')
        }),
        ('Opzioni', {
            'fields': ('is_recurring', 'specific_date', 'is_active')
        })
    )
    
    def associate_name(self, obj):
        return obj.associate.user.get_full_name()
    associate_name.short_description = "Associato"
    associate_name.admin_order_field = 'associate__user__last_name'
    
    def day_display(self, obj):
        if obj.specific_date:
            return f"Specifica: {obj.specific_date}"
        return obj.get_day_of_week_display()
    day_display.short_description = "Giorno"
    
    def time_range(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    time_range.short_description = "Orario"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('associate__user')  