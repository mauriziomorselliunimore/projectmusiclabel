from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, time
from messaging.models import Message, Notification, Conversation
from .models import Associate, PortfolioItem, Availability
from .forms import AssociateForm, PortfolioItemForm, AvailabilityForm

def associate_list(request):
    """Lista tutti gli associati con ricerca"""
    query = request.GET.get('search', '')
    skill_filter = request.GET.get('skill', '')
    location_filter = request.GET.get('location', '')
    
    associates = Associate.objects.filter(is_active=True, is_available=True)
    
    if query:
        associates = associates.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(skills__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if skill_filter:
        associates = associates.filter(skills__icontains=skill_filter)
    
    if location_filter:
        associates = associates.filter(location__icontains=location_filter)
    
    context = {
        'associates': associates,
        'search_query': query,
        'skill_filter': skill_filter,
        'location_filter': location_filter,
    }
    return render(request, 'associates/associate_list.html', context)

def associate_detail(request, pk):
    """Dettaglio singolo associato con integrazione messaggistica e booking"""
    associate = get_object_or_404(Associate, pk=pk, is_active=True)
    portfolio_items = associate.portfolio_items.all()
    
    # Check if user can send messages
    can_message = (
        request.user.is_authenticated and 
        request.user != associate.user and
        hasattr(request.user, 'profile')
    )
    
    # Check if user can book (only artists can book associates)
    can_book = (
        request.user.is_authenticated and 
        hasattr(request.user, 'artist') and
        request.user != associate.user and
        associate.is_available
    )
    
    # Get existing conversation if any - FIXED VERSION
    existing_conversation = None
    if request.user.is_authenticated and request.user != associate.user:
        try:
            existing_conversation = Conversation.objects.filter(
                Q(participant_1=request.user, participant_2=associate.user) |
                Q(participant_1=associate.user, participant_2=request.user)
            ).first()
        except Exception:
            # Se ci sono errori con il modello Conversation, ignora
            existing_conversation = None

    # Get recent bookings with this associate (for reputation)
    recent_bookings = None
    if request.user.is_authenticated and hasattr(request.user, 'artist'):
        try:
            from booking.models import Booking
            recent_bookings = Booking.objects.filter(
                artist=request.user.artist,
                associate=associate,
                status__in=['completed', 'confirmed']
            ).order_by('-session_date')[:3]
        except Exception:
            # Se ci sono errori con i booking, ignora
            recent_bookings = None
    
    context = {
        'associate': associate,
        'portfolio_items': portfolio_items,
        'is_owner': request.user == associate.user,
        'can_message': can_message,
        'can_book': can_book,
        'existing_conversation': existing_conversation,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'associates/associate_detail.html', context)


@login_required
def associate_create(request):
    """Crea profilo associato"""
    # Check if user already has an associate profile
    if hasattr(request.user, 'associate'):
        messages.info(request, 'Hai già un profilo associato!')
        return redirect('associates:detail', pk=request.user.associate.pk)
    
    if request.method == 'POST':
        form = AssociateForm(request.POST)
        if form.is_valid():
            associate = form.save(commit=False)
            associate.user = request.user
            associate.save()
            messages.success(request, 'Profilo associato creato con successo!')
            return redirect('associates:detail', pk=associate.pk)
    else:
        form = AssociateForm()
    
    return render(request, 'associates/associate_form.html', {'form': form, 'title': 'Crea Profilo Associato'})

@login_required
def associate_edit(request, pk):
    """Modifica profilo associato"""
    associate = get_object_or_404(Associate, pk=pk)
    
    # Check ownership
    if associate.user != request.user:
        messages.error(request, 'Non hai i permessi per modificare questo profilo!')
        return redirect('associates:detail', pk=pk)
    
    if request.method == 'POST':
        form = AssociateForm(request.POST, instance=associate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('associates:detail', pk=pk)
    else:
        form = AssociateForm(instance=associate)
    
    return render(request, 'associates/associate_form.html', {'form': form, 'title': 'Modifica Profilo'})

@login_required
def portfolio_add(request):
    """Aggiungi elemento al portfolio"""
    if not hasattr(request.user, 'associate'):
        messages.error(request, 'Devi avere un profilo associato per aggiungere elementi al portfolio!')
        return redirect('associates:create')
    
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_item = form.save(commit=False)
            portfolio_item.associate = request.user.associate
            portfolio_item.save()
            messages.success(request, f'Elemento "{portfolio_item.title}" aggiunto al portfolio!')
            return redirect('associates:detail', pk=request.user.associate.pk)
    else:
        form = PortfolioItemForm()
    
    return render(request, 'associates/portfolio_form.html', {'form': form})

@login_required
def portfolio_delete(request, pk):
    """Elimina elemento portfolio"""
    portfolio_item = get_object_or_404(PortfolioItem, pk=pk)
    
    # Check ownership
    if portfolio_item.associate.user != request.user:
        messages.error(request, 'Non hai i permessi per eliminare questo elemento!')
        return redirect('associates:detail', pk=portfolio_item.associate.pk)
    
    if request.method == 'POST':
        portfolio_item.delete()
        messages.success(request, 'Elemento eliminato dal portfolio!')
        return redirect('associates:detail', pk=portfolio_item.associate.pk)
    
    return render(request, 'associates/portfolio_confirm_delete.html', {'portfolio_item': portfolio_item})

@login_required
def quick_message(request):
    """Send quick message via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
    try:
        import json
        data = json.loads(request.body)
        
        recipient_id = data.get('recipient_id')
        message_text = data.get('message')
        subject = data.get('subject', 'Nuovo messaggio')
        message_type = data.get('message_type', 'general')
        
        if not recipient_id or not message_text:
            return JsonResponse({'success': False, 'error': 'Dati mancanti'})
        
        recipient = User.objects.get(id=recipient_id)
        
        if request.user == recipient:
            return JsonResponse({'success': False, 'error': 'Non puoi inviare messaggi a te stesso'})
        
        # Get or create conversation
        conversation = Conversation.get_or_create_conversation(request.user, recipient)
        
        # Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            subject=subject,
            message=message_text,
            message_type=message_type
        )
        
        # Create notification
        Notification.objects.create(
            user=recipient,
            notification_type='new_message',
            title=f'Nuovo messaggio da {request.user.get_full_name()}',
            message=f'Oggetto: {subject}',
            action_url=message.get_absolute_url(),
            related_message=message,
            related_user=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'conversation_url': conversation.get_absolute_url()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def availability_manage(request):
    """Gestione disponibilità associate"""
    if not hasattr(request.user, 'associate'):
        messages.error(request, 'Devi avere un profilo associato per gestire la disponibilità!')
        return redirect('associates:create')
    
    associate = request.user.associate
    availability_slots = associate.availabilities.all().order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        # Inizializzamo il form con l'associate
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            try:
                availability = form.save(commit=False)
                availability.associate = associate
                availability.save()
                messages.success(request, 'Disponibilità aggiunta con successo!')
                return redirect('associates:availability_manage')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    form.add_error(field if field != '__all__' else None, error)
    else:
        form = AvailabilityForm()
    
    context = {
        'form': form,
        'availability_slots': availability_slots,
        'days': dict(Availability.DAYS_OF_WEEK)
    }
    return render(request, 'associates/availability_manage.html', context)

@login_required
def availability_delete(request, pk):
    """Elimina slot disponibilità"""
    availability = get_object_or_404(Availability, pk=pk)
    
    # Check ownership
    if availability.associate.user != request.user:
        messages.error(request, 'Non hai i permessi per eliminare questo slot di disponibilità!')
        return redirect('associates:availability_manage')
    
    if request.method == 'POST':
        availability.delete()
        messages.success(request, 'Slot di disponibilità eliminato!')
        return redirect('associates:availability_manage')
    
    context = {
        'availability': availability,
        'day': dict(Availability.DAYS_OF_WEEK)[availability.day_of_week]
    }
    return render(request, 'associates/availability_confirm_delete.html', context)

@login_required
def availability_update(request, pk):
    """Modifica slot disponibilità"""
    availability = get_object_or_404(Availability, pk=pk)
    
    # Check ownership
    if availability.associate.user != request.user:
        messages.error(request, 'Non hai i permessi per modificare questo slot di disponibilità!')
        return redirect('associates:availability_manage')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Slot di disponibilità aggiornato!')
                return redirect('associates:availability_manage')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
    else:
        form = AvailabilityForm(instance=availability)
    
    context = {
        'form': form,
        'availability': availability,
        'day': dict(Availability.DAYS_OF_WEEK)[availability.day_of_week]
    }
    return render(request, 'associates/availability_form.html', context)