
from django.contrib import admin
from .models import Availability

# Booking is registered in core/admin.py, do not register here to avoid AlreadyRegistered error

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
	list_display = ['associate', 'day_of_week', 'start_time', 'end_time', 'is_recurring', 'specific_date', 'is_active']
	list_filter = ['day_of_week', 'is_recurring', 'is_active', 'associate']
	search_fields = ['associate__user__username']
	date_hierarchy = 'specific_date'




