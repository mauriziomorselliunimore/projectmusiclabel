from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # Booking URLs
    path('calendar/<int:associate_id>/', views.booking_calendar, name='calendar'),
    path('create/<int:associate_id>/', views.create_booking, name='create'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/update-status/', views.booking_status_update, name='update_status'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Gestione disponibilità
    path('availability/manage/', views.manage_availability, name='manage_availability'),
    path('availability/toggle/<int:availability_id>/', views.toggle_availability, name='toggle_availability'),
    path('availability/delete/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    
    # API URLs
    path('api/available-slots/<int:associate_id>/', views.api_available_slots, name='api_slots'),
]