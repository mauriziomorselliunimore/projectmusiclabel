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
    
    # API URLs
    path('api/available-slots/<int:associate_id>/', views.api_available_slots, name='api_slots'),
]