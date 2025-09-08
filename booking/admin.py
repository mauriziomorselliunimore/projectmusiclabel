
from django.contrib import admin
from .models import Booking, Availability, QuoteRequest

# Booking is registered in core/admin.py, do not register here to avoid AlreadyRegistered error

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
	list_display = ['associate', 'day_of_week', 'start_time', 'end_time', 'is_recurring', 'specific_date', 'is_active']
	list_filter = ['day_of_week', 'is_recurring', 'is_active', 'associate']
	search_fields = ['associate__user__username']
	date_hierarchy = 'specific_date'

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
	list_display = ['artist', 'associate', 'status', 'created_at', 'responded_at']
	list_filter = ['status', 'created_at', 'responded_at']
	search_fields = ['artist__stage_name', 'associate__user__username', 'message', 'response']
	date_hierarchy = 'created_at'



