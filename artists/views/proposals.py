from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models.collaboration import CollaborationProposal
from messaging.models import Message, Notification
import json

@login_required
def proposal_list(request):
    """Lista le proposte di collaborazione ricevute"""
    proposals = CollaborationProposal.objects.filter(receiver=request.user)
    
    # Apply filters
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    sort = request.GET.get('sort', '-created_at')
    
    if status_filter:
        proposals = proposals.filter(status=status_filter)
    
    if type_filter:
        proposals = proposals.filter(type=type_filter)
    
    # Apply sorting
    proposals = proposals.order_by(sort)
    
    context = {
        'proposals': proposals,
    }
    return render(request, 'artists/proposals.html', context)

@login_required
def update_proposal_status(request, proposal_id):
    """Aggiorna lo stato di una proposta"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo non consentito'})
        
    proposal = get_object_or_404(CollaborationProposal, id=proposal_id, receiver=request.user)
    
    try:
        data = json.loads(request.body)
        status = data.get('status')
        message = data.get('message', '')
        
        if status not in ['accepted', 'rejected']:
            return JsonResponse({'success': False, 'error': 'Stato non valido'})
        
        proposal.status = status
        proposal.response_message = message
        proposal.save()
        
        # Create notification for sender
        status_display = 'accettata' if status == 'accepted' else 'rifiutata'
        notification_message = f"La tua proposta di collaborazione è stata {status_display}"
        if message:
            notification_message += f"\nNote: {message}"
            
        Notification.objects.create(
            user=proposal.sender,
            notification_type='proposal_update',
            title=f'Proposta {status_display}',
            message=notification_message,
            action_url=f'/artists/proposals/{proposal.id}/',
            related_message=proposal.original_message
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def counter_proposal(request, proposal_id):
    """Invia una controproposta"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo non consentito'})
        
    proposal = get_object_or_404(CollaborationProposal, id=proposal_id, receiver=request.user)
    
    try:
        data = json.loads(request.body)
        budget = data.get('budget')
        notes = data.get('notes')
        
        if not notes:
            return JsonResponse({'success': False, 'error': 'Note richieste'})
            
        proposal.status = 'counter'
        proposal.counter_budget = budget
        proposal.counter_notes = notes
        proposal.save()
        
        # Create notification for sender
        Notification.objects.create(
            user=proposal.sender,
            notification_type='counter_proposal',
            title='Nuova controproposta',
            message=f'Hai ricevuto una controproposta per la tua richiesta di collaborazione\n\n{notes}',
            action_url=f'/artists/proposals/{proposal.id}/',
            related_message=proposal.original_message
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def create_proposal_from_message(sender, receiver, message_obj, proposal_data):
    """Crea una proposta di collaborazione da un messaggio"""
    try:
        proposal = CollaborationProposal.objects.create(
            sender=sender,
            receiver=receiver,
            type=proposal_data['type'],
            budget=proposal_data.get('budget'),
            description=proposal_data['description'],
            timeline=proposal_data['timeline'],
            mode=proposal_data['mode'],
            reference_links='\n'.join(proposal_data.get('references', [])),
            original_message=message_obj
        )
        
        # Create notification
        Notification.objects.create(
            user=receiver,
            notification_type='new_proposal',
            title=f'Nuova proposta di collaborazione da {sender.get_full_name()}',
            message=f'Tipo: {proposal.get_type_display()}\nBudget: {"€" + str(proposal.budget) if proposal.budget else "Da concordare"}',
            action_url=f'/artists/proposals/{proposal.id}/',
            related_message=message_obj
        )
        
        return proposal
    except Exception as e:
        print(f"Errore nella creazione della proposta: {e}")
        return None
