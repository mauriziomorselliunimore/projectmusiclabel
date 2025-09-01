from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from artists.models import Artist
from associates.models import Associate
from booking.models import Booking
from messaging.models import Message
from django.contrib.admin.models import LogEntry

@staff_member_required
def control_panel(request):
    """Vista per il pannello di controllo admin"""
    context = {
        'title': 'Control Panel',
        # Statistiche
        'artist_count': Artist.objects.count(),
        'associate_count': Associate.objects.count(),
        'booking_count': Booking.objects.count(),
        'message_count': Message.objects.count(),
        # Attività recenti
        'recent_activities': LogEntry.objects.select_related('user')[:10],
    }
    
    return render(request, 'admin/control_panel.html', context)
