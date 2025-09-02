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
        if form.is_valid():
            booking = form.save(commit=False)
            booking.artist = request.user.artist
            booking.associate = associate
            booking.status = 'pending'
            booking.save()
            
            messages.success(request, 'Richiesta di prenotazione inviata con successo!')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('booking:detail', args=[booking.pk])
                })
            return redirect('booking:detail', pk=booking.pk)
        
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    else:
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
    
    # Controlla quali slot sono già prenotati
    booked_slots = Booking.objects.filter(
        associate=associate,
        session_date__date__range=[start_date, end_date],
        status__in=['pending', 'confirmed']
    ).values_list('session_date', flat=True)
    
    for slot in availabilities:
        is_booked = any(
            booked.date() == slot.start_time.date() and 
            booked.hour == slot.start_time.hour
            for booked in booked_slots
        )
        available_slots.append({
            'id': slot.id,
            'start_time': slot.start_time,
            'duration_hours': slot.duration_hours,
            'is_booked': is_booked
        })
    
    context = {
        'form': form,
        'associate': associate,
        'artist': request.user.artist,
        'available_slots': available_slots
    }
    return render(request, 'booking/booking_form.html', context)
            
            # Import qui per evitare circular import
            from messaging.models import Notification, Message
            
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
            from messaging.models import Conversation
            conversation = Conversation.get_or_create_conversation(request.user, associate.user)
            
            # Messaggio automatico
            Message.objects.create(
                sender=request.user,
                recipient=associate.user,
                conversation=conversation,
                message_type='booking_request',
                subject=f'Richiesta prenotazione - {booking.get_booking_type_display()}',
                message=f'Ciao {associate.user.first_name},\n\n'
                       f'Vorrei prenotare una sessione di {booking.get_booking_type_display()} '
                       f'per il {booking.session_date.strftime("%d/%m/%Y alle %H:%M")}.\n\n'
                       f'Durata: {duration_hours} ore\n'
                       f'Località: {location or "Da definire"}\n'
                       f'Note: {notes or "Nessuna nota aggiuntiva"}\n\n'
                       f'Fammi sapere se va bene!\n\n'
                       f'{request.user.get_full_name()} ({request.user.artist.stage_name})',
                related_booking=booking
            )
            
            messages.success(request, 'Richiesta di prenotazione inviata con successo!')
            return redirect('booking:detail', pk=booking.pk)
            
        except Exception as e:
            messages.error(request, f'Errore nella prenotazione: {str(e)}')
            return redirect('booking:calendar', associate_id=associate.pk)
    
    # GET request - mostra form
    return render(request, 'booking/create_form.html', {
        'associate': associate,
        'artist': request.user.artist
    })

@login_required
def booking_detail(request, pk):
    """Dettaglio singola prenotazione"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Verifica permessi
    if request.user not in [booking.artist.user, booking.associate.user]:
        messages.error(request, 'Non hai permesso di visualizzare questa prenotazione!')
        return redirect('core:home')
    
    is_artist = request.user == booking.artist.user
    is_associate = request.user == booking.associate.user
    
    context = {
        'booking': booking,
        'is_artist': is_artist,
        'is_associate': is_associate,
        'can_modify': booking.status == 'pending' and booking.is_upcoming,
    }
    return render(request, 'booking/detail.html', context)

@login_required
@require_http_methods(["POST"])
def booking_status_update(request, pk):
    """Aggiorna status booking (solo associati)"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.user != booking.associate.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Solo l\'associato può modificare lo status!'}, status=403)
        messages.error(request, 'Solo l\'associato può modificare lo status!')
        return redirect('booking:detail', pk=pk)
    
    new_status = request.POST.get('status')
    if new_status not in ['confirmed', 'cancelled']:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Status non valido!'}, status=400)
        messages.error(request, 'Status non valido!')
        return redirect('booking:detail', pk=pk)
    
    try:
        old_status = booking.status
        booking.status = new_status
        booking.save()
        
        # Import qui per evitare circular import
        from messaging.models import Notification, Message, Conversation
        
        # Notifica artista
        status_msg = 'confermata' if new_status == 'confirmed' else 'cancellata'
        Notification.objects.create(
            user=booking.artist.user,
            notification_type=f'booking_{new_status}',
            title=f'Prenotazione {status_msg}',
            message=f'La tua prenotazione del {booking.session_date.strftime("%d/%m/%Y alle %H:%M")} è stata {status_msg}.',
            related_booking=booking
        )
        
        # Crea o recupera la conversazione
        conversation = Conversation.get_or_create_conversation(
            request.user,
            booking.artist.user
        )
        
        # Invia messaggio di conferma/cancellazione
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=booking.artist.user,
            message_type='booking_update',
            subject=f'Prenotazione {status_msg}',
            message=f'Ciao {booking.artist.user.first_name},\n\n'
                   f'La tua prenotazione del {booking.session_date.strftime("%d/%m/%Y alle %H:%M")} '
                   f'è stata {status_msg}.\n\n'
                   f'Tipo: {booking.get_booking_type_display()}\n'
                   f'Durata: {booking.duration_hours} ore\n'
                   f'Location: {booking.location or "Da definire"}\n\n'
                   f'Saluti,\n{request.user.get_full_name()}',
            related_booking=booking
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Prenotazione {status_msg} con successo!',
                'redirect_url': request.build_absolute_uri(booking.get_absolute_url())
            })
        
        messages.success(request, f'Prenotazione {status_msg} con successo!')
        return redirect('booking:detail', pk=pk)
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, f'Errore: {str(e)}')
        return redirect('booking:detail', pk=pk)

@login_required
def my_bookings(request):
    """Lista booking utente (artista o associato)"""
    if hasattr(request.user, 'artist'):
        bookings = Booking.objects.filter(artist=request.user.artist)
        user_type = 'artist'
    elif hasattr(request.user, 'associate'):
        bookings = Booking.objects.filter(associate=request.user.associate)
        user_type = 'associate'
    else:
        bookings = Booking.objects.none()
        user_type = None
    
    # Filtri
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Ordina per data
    bookings = bookings.select_related('artist__user', 'associate__user').order_by('-session_date')
    
    context = {
        'bookings': bookings,
        'user_type': user_type,
        'status_filter': status_filter,
        'status_choices': Booking.BOOKING_STATUS,
    }
    return render(request, 'booking/my_bookings.html', context)

@csrf_exempt
@login_required
def api_available_slots(request, associate_id):
    """API per slots disponibili in una data specifica"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        associate = Associate.objects.get(id=associate_id, is_active=True)
        date_str = request.GET.get('date')
        
        if not date_str:
            return JsonResponse({'error': 'Date parameter required'}, status=400)
        
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = target_date.weekday()  # 0=Monday
        
        # Get disponibilità per quel giorno
        availabilities = associate.availability_slots.filter(
            Q(day_of_week=day_of_week, is_recurring=True) |
            Q(specific_date=target_date, is_recurring=False),
            is_active=True
        )
        
        # Get booking esistenti per quel giorno
        existing_bookings = Booking.objects.filter(
            associate=associate,
            session_date__date=target_date,
            status__in=['pending', 'confirmed']
        )
        
        # Calcola slots liberi
        available_slots = []
        for availability in availabilities:
            current_time = availability.start_time
            end_time = availability.end_time
            
            while current_time < end_time:
                slot_datetime = datetime.combine(target_date, current_time)
                slot_datetime = timezone.make_aware(slot_datetime)
                
                # Verifica se slot è libero
                is_free = True
                for booking in existing_bookings:
                    if (slot_datetime >= booking.session_date and 
                        slot_datetime < booking.session_date + timedelta(hours=booking.duration_hours)):
                        is_free = False
                        break
                
                if is_free and slot_datetime > timezone.now():
                    available_slots.append({
                        'time': current_time.strftime('%H:%M'),
                        'datetime': slot_datetime.isoformat()
                    })
                
                # Avanza di 1 ora
                current_time = (datetime.combine(target_date, current_time) + timedelta(hours=1)).time()
        
        return JsonResponse({'available_slots': available_slots})
        
    except Associate.DoesNotExist:
        return JsonResponse({'error': 'Associate not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)