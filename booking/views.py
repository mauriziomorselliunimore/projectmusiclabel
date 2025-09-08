from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, time
from django.core.exceptions import PermissionDenied
from .forms import AvailabilityForm
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
    
    # Get disponibilità per le prossime 4 settimane
    start_date = timezone.now().date()
    end_date = start_date + timedelta(weeks=4)
    
    # Get disponibilità ricorrenti e specifiche
    recurring_slots = associate.availability_slots.filter(
        is_recurring=True,
        is_active=True
    ).order_by('day_of_week', 'start_time')
    
    specific_slots = associate.availability_slots.filter(
        is_recurring=False,
        is_active=True,
        specific_date__gte=start_date,
        specific_date__lte=end_date
    ).order_by('specific_date', 'start_time')
    
    # Combina le disponibilità per la visualizzazione
    available_slots = []
    
    # Aggiungi slot ricorrenti per le prossime 4 settimane
    current_date = start_date
    while current_date <= end_date:
        for slot in recurring_slots:
            if slot.day_of_week == current_date.weekday():
                available_slots.append({
                    'date': current_date,
                    'start_time': slot.start_time,
                    'end_time': slot.end_time
                })
        current_date += timedelta(days=1)
    
    # Aggiungi slot specifici
    for slot in specific_slots:
        available_slots.append({
            'date': slot.specific_date,
            'start_time': slot.start_time,
            'end_time': slot.end_time
        })
    
    # Ordina gli slot per data e ora
    available_slots.sort(key=lambda x: (x['date'], x['start_time']))

    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and not form.is_valid():
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.artist = request.user.artist
                booking.associate = associate
                booking.status = 'pending'
                booking.save()
                
                # Import qui per evitare circular import
                from messaging.models import Notification, Message, Conversation
                
                # Crea notifica per l'associato
                try:
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
                except Exception as e:
                    messages.warning(request, f'Impossibile creare la notifica: {str(e)}')
                    conversation = Conversation.get_or_create_conversation(request.user, associate.user)

                Message.objects.create(
                    sender=request.user,
                    recipient=associate.user,
                    conversation=conversation,
                    message_type='booking_request',
                    subject=f'Richiesta prenotazione - {booking.get_booking_type_display()}',
                    message=(
                        f"""Ciao {associate.user.first_name},

Vorrei prenotare una sessione di {booking.get_booking_type_display()} per il {booking.session_date.strftime('%d/%m/%Y alle %H:%M')}.

Durata: {booking.duration_hours} ore
Località: {booking.location or 'Da definire'}
Note: {booking.notes or 'Nessuna nota aggiuntiva'}

Fammi sapere se va bene!

{request.user.get_full_name()} ({request.user.artist.stage_name})"""
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
        Q(
            is_recurring=True,
            is_active=True
        ) |
        Q(
            is_recurring=False,
            specific_date__gte=start_date,
            specific_date__lte=end_date,
            is_active=True
        )
    ).order_by('day_of_week', 'start_time')

    # Ottieni i booking esistenti
    existing_bookings = Booking.objects.filter(
        associate=associate,
        session_date__date__range=[start_date, end_date],
        status__in=['pending', 'confirmed']
    ).select_related('artist__user')

    context = {
        'form': form,
        'associate': associate,
        'artist': request.user.artist,
        'recurring_slots': recurring_slots,
        'specific_slots': specific_slots,
        'available_slots': available_slots,  # Aggiungi gli slot ordinati
        'existing_bookings': existing_bookings,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
def booking_detail(request, pk):
    """Dettaglio singola prenotazione"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Verifica che l'utente possa vedere questa prenotazione
    if not (request.user == booking.artist.user or request.user == booking.associate.user):
        messages.error(request, 'Non hai i permessi per vedere questa prenotazione.')
        return redirect('home')
    
    context = {
        'booking': booking,
        'artist': booking.artist,
        'associate': booking.associate
    }
    return render(request, 'booking/detail.html', context)

@login_required
def booking_status_update(request, pk):
    """Aggiorna lo stato di una prenotazione"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Solo l'associato può aggiornare lo stato
    if request.user != booking.associate.user:
        messages.error(request, 'Solo l\'associato può aggiornare lo stato della prenotazione.')
        return redirect('booking:detail', pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['confirmed', 'rejected', 'completed']:
            old_status = booking.status
            booking.status = new_status
            booking.save()
            
            # Import qui per evitare circular import
            from messaging.models import Notification, Message
            
            # Crea notifica per l'artista
            status_display = dict(Booking.STATUS_CHOICES)[new_status]
            Notification.objects.create(
                user=booking.artist.user,
                notification_type=f'booking_{new_status}',
                title=f'Prenotazione {status_display.lower()}',
                message=f'La tua richiesta di prenotazione è stata {status_display.lower()}',
                related_booking=booking,
                action_url=f'/booking/{booking.pk}/'
            )
            
            # Crea messaggio
            Message.objects.create(
                sender=request.user,
                recipient=booking.artist.user,
                conversation=Message.objects.filter(
                    related_booking=booking
                ).first().conversation,
                message_type=f'booking_{new_status}',
                subject=f'Prenotazione {status_display}',
                message=f'La tua richiesta di prenotazione è stata {status_display.lower()}.',
                related_booking=booking
            )
            
            messages.success(request, f'Stato della prenotazione aggiornato a {status_display}')
        else:
            messages.error(request, 'Stato non valido')
            
    return redirect('booking:detail', pk=pk)

@login_required
def my_bookings(request):
    """Lista delle prenotazioni dell'utente"""
    # Se è admin, mostra tutte le prenotazioni
    if request.user.is_staff:
        bookings = Booking.objects.all().select_related(
            'artist__user', 'associate__user'
        ).order_by('-created_at')
        return render(request, 'booking/admin_bookings.html', {'bookings': bookings})
        
    if hasattr(request.user, 'artist'):
        # Se è un artista, mostra le sue prenotazioni
        bookings = Booking.objects.filter(
            artist=request.user.artist
        ).select_related('associate__user').order_by('-created_at')
    elif hasattr(request.user, 'associate'):
        # Se è un associato, mostra le prenotazioni ricevute
        bookings = Booking.objects.filter(
            associate=request.user.associate
        ).select_related('artist__user').order_by('-created_at')
    else:
        messages.error(request, 'Non hai i permessi per vedere le prenotazioni.')
        return redirect('core:home')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/my_bookings.html', context)

@csrf_exempt
@require_http_methods(["GET"])
def api_available_slots(request, associate_id):
    """API per ottenere gli slot disponibili di un associato"""
    try:
        associate = get_object_or_404(Associate, id=associate_id)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return JsonResponse({'error': 'Devi specificare start_date e end_date'}, status=400)
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato data non valido. Usa YYYY-MM-DD'}, status=400)
        # Get disponibilità
        availabilities = associate.availability_slots.filter(
            start_time__date__range=[start_date, end_date],
            is_active=True
        ).order_by('start_time')
        
        # Get prenotazioni esistenti
        existing_bookings = Booking.objects.filter(
            associate=associate,
            session_date__date__range=[start_date, end_date],
            status__in=['pending', 'confirmed']
        )
        
        # Formatta le disponibilità
        available_slots = []
        for slot in availabilities:
            if not existing_bookings.filter(session_date__range=[
                slot.start_time, slot.end_time
            ]).exists():
                available_slots.append({
                    'id': slot.id,
                    'start': slot.start_time.isoformat(),
                    'end': slot.end_time.isoformat(),
                    'title': 'Disponibile'
                })
        
        return JsonResponse({
            'slots': available_slots,
            'timezone': str(timezone.get_current_timezone())
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def manage_availability(request):
    """Vista per gestire le disponibilità dell'associato"""
    if not hasattr(request.user, 'associate'):
        messages.error(request, 'Solo gli associati possono gestire le disponibilità')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.associate = request.user.associate
            availability.save()
            messages.success(request, 'Disponibilità aggiunta con successo!')
            return redirect('booking:manage_availability')
    else:
        form = AvailabilityForm()
    
    # Get disponibilità esistenti
    availabilities = request.user.associate.availability_slots.all().order_by(
        'is_recurring', 'day_of_week', 'specific_date', 'start_time'
    )
    
    context = {
        'form': form,
        'availabilities': availabilities
    }
    return render(request, 'booking/manage_availability.html', context)

@login_required
def toggle_availability(request, availability_id):
    """Attiva/disattiva una disponibilità"""
    availability = get_object_or_404(Availability, id=availability_id)
    
    # Verifica che l'utente sia il proprietario
    if availability.associate.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        availability.is_active = not availability.is_active
        availability.save()
        messages.success(request, 'Disponibilità aggiornata con successo!')
    
    return redirect('booking:manage_availability')

@login_required
def delete_availability(request, availability_id):
    """Elimina una disponibilità"""
    availability = get_object_or_404(Availability, id=availability_id)
    
    # Verifica che l'utente sia il proprietario
    if availability.associate.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        availability.delete()
        messages.success(request, 'Disponibilità eliminata con successo!')
    
    return redirect('booking:manage_availability')

@login_required
def view_availability(request, associate_id):
    """Vista pubblica delle disponibilità di un associato"""
    associate = get_object_or_404(Associate, id=associate_id)
    
    # Get tutte le disponibilità attive
    availabilities = associate.availability_slots.all().order_by(
        'is_recurring', 'day_of_week', 'specific_date', 'start_time'
    )
    
    context = {
        'associate': associate,
        'availabilities': availabilities,
        'today': timezone.now().date()
    }
    return render(request, 'booking/availability_view.html', context)