from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Booking, Availability
from .forms import BookingForm
from artists.models import Artist
from associates.models import Associate
from accounts.models import Profile

@login_required
def booking_calendar(request, associate_id):
    """Calendario booking per un associato specifico"""
    associate = get_object_or_404(Associate, id=associate_id, is_active=True)
    
    # Verifica che l'utente possa fare booking
    if not hasattr(request.user, 'artist'):
        messages.error(request, 'Solo gli artisti possono prenotare sessioni!')
        return redirect('associates:detail', pk=associate.pk)
    
    # Get disponibilità associate
    availabilities = associate.availability_slots.filter(is_active=True)
    
    # Get bookings esistenti per le prossime 4 settimane
    start_date = timezone.now().date()
    end_date = start_date + timedelta(weeks=4)
    
    existing_bookings = Booking.objects.filter(
        associate=associate,
        session_date__date__range=[start_date, end_date],
        status__in=['pending', 'confirmed']
    ).select_related('artist__user')
    
    context = {
        'associate': associate,
        'artist': request.user.artist,
        'availabilities': availabilities,
        'existing_bookings': existing_bookings,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'booking/calendar.html', context)

@login_required
def create_booking(request, associate_id):
    """Crea nuova prenotazione"""
    associate = get_object_or_404(Associate, id=associate_id, is_active=True)
    
    if not hasattr(request.user, 'artist'):
        messages.error(request, 'Solo gli artisti possono prenotare sessioni!')
        return redirect('associates:detail', pk=associate.pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and not form.is_valid():
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        
        try:
            if form.is_valid():
                booking = form.save(commit=False)
                booking.artist = request.user.artist
                booking.associate = associate
                booking.status = 'pending'
                booking.save()
                
                # Import qui per evitare circular import
                from messaging.models import Notification, Message, Conversation
                
                # Crea notifica per l'associato
                Notification.objects.create(
                    user=associate.user,
                    notification_type='booking_request',
                    title=f'Nuova richiesta prenotazione da {request.user.artist.stage_name}',
                    message=f'Richiesta per {booking.get_booking_type_display()} il {booking.session_date.strftime("%d/%m/%Y alle %H:%M")}',
                    related_booking=booking,
                    action_url=f'/booking/{booking.pk}/'
                )
                
                # Ottieni o crea conversazione
                conversation = Conversation.get_or_create_conversation(request.user, associate.user)
                
                # Messaggio automatico
                Message.objects.create(
                    sender=request.user,
                    recipient=associate.user,
                    conversation=conversation,
                    message_type='booking_request',
                    subject=f'Richiesta prenotazione - {booking.get_booking_type_display()}',
                    message=(
                        f'Ciao {associate.user.first_name},\n\n'
                        f'Vorrei prenotare una sessione di {booking.get_booking_type_display()} '
                        f'per il {booking.session_date.strftime("%d/%m/%Y alle %H:%M")}.\n\n'
                        f'Durata: {booking.duration_hours} ore\n'
                        f'Località: {booking.location or "Da definire"}\n'
                        f'Note: {booking.notes or "Nessuna nota aggiuntiva"}\n\n'
                        f'Fammi sapere se va bene!\n\n'
                        f'{request.user.get_full_name()} ({request.user.artist.stage_name})'
                    ),
                    related_booking=booking
                )
                
                messages.success(request, 'Richiesta di prenotazione inviata con successo!')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('booking:detail', args=[booking.pk])
                    })
                return redirect('booking:detail', pk=booking.pk)
        
        except Exception as e:
            messages.error(request, f'Errore nella prenotazione: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            return redirect('booking:calendar', associate_id=associate.pk)
    
    # GET request - mostra form
    initial = {
        'booking_type': 'recording',
        'duration_hours': 2
    }
    form = BookingForm(initial=initial)

    # Get le disponibilità dell'associato per le prossime 4 settimane
    start_date = timezone.now().date()
    end_date = start_date + timedelta(weeks=4)
    
    available_slots = []
    availabilities = associate.availability_slots.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        is_active=True
    ).order_by('start_time')

    context = {
        'form': form,
        'associate': associate,
        'artist': request.user.artist,
        'available_slots': available_slots
    }
    return render(request, 'booking/booking_form.html', context)