from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.management import call_command
from .models import Message
from artists.views.proposals import create_proposal_from_message
import re

@receiver(post_save, sender=User)
def send_welcome_message(sender, instance, created, **kwargs):
    """Invia un messaggio di benvenuto quando viene creato un nuovo utente"""
    if created:  # Solo per nuovi utenti
        call_command('send_welcome_messages')

@receiver(post_save, sender=Message)
def handle_collaboration_message(sender, instance, created, **kwargs):
    """Gestisce la creazione automatica di proposte quando viene inviato un messaggio di collaborazione"""
    if not created or instance.message_type != 'collaboration':
        return
        
    # Parse message content to extract proposal data
    message_lines = instance.text.split('\n')
    proposal_data = {}
    
    for line in message_lines:
        if line.startswith('Tipo: '):
            proposal_data['type'] = line.replace('Tipo: ', '').strip()
        elif line.startswith('Budget: '):
            budget_str = line.replace('Budget: €', '').replace('Da concordare', '').strip()
            try:
                proposal_data['budget'] = float(budget_str) if budget_str else None
            except ValueError:
                proposal_data['budget'] = None
        elif line.startswith('Timeline: '):
            proposal_data['timeline'] = line.replace('Timeline: ', '').strip()
        elif line.startswith('Modalità: '):
            proposal_data['mode'] = line.replace('Modalità: ', '').strip()
            
    # Extract description from between "DESCRIZIONE PROGETTO:" and the next empty line
    description_match = re.search(r'DESCRIZIONE PROGETTO:\n(.*?)(?=\n\n|\Z)', instance.text, re.DOTALL)
    if description_match:
        proposal_data['description'] = description_match.group(1).strip()
    
    # Create the proposal
    create_proposal_from_message(
        sender=instance.sender,
        receiver=instance.recipient,
        message_obj=instance,
        proposal_data=proposal_data
    )
