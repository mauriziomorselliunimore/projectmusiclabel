from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_template_email(template_name, context, subject, recipient_list, from_email=None):
    """
    Invia una email usando un template HTML via SendGrid
    
    Args:
        template_name (str): Nome del template email (senza estensione)
        context (dict): Contesto per il template
        subject (str): Oggetto dell'email
        recipient_list (list): Lista di indirizzi email destinatari
        from_email (str, optional): Email mittente. Default None (usa VERIFIED_SENDER_EMAIL)
    """
    try:
        from_email = from_email or settings.VERIFIED_SENDER_EMAIL
        if not from_email:
            logger.error("VERIFIED_SENDER_EMAIL non configurato")
            return False
            
        # Aggiunge il prefisso all'oggetto
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
        
        # Renderizza il template HTML
        html_content = render_to_string(f'emails/{template_name}.html', context)
        text_content = strip_tags(html_content)
        
        # Crea il messaggio
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list,
            headers={'X-SMTPAPI': '{"category": ["' + template_name + '"]}'}
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Invia e logga il risultato
        success = msg.send()
        if success:
            logger.info(f"Email '{template_name}' inviata con successo a {', '.join(recipient_list)}")
        else:
            logger.error(f"Errore nell'invio dell'email '{template_name}' a {', '.join(recipient_list)}")
        return success
        
    except Exception as e:
        logger.exception(f"Errore nell'invio dell'email '{template_name}': {str(e)}")

def send_welcome_email(user):
    """Invia email di benvenuto a un nuovo utente"""
    from django.urls import reverse
    context = {
        'user': user,
        'login_url': f"{settings.SITE_URL}{reverse('accounts:profile')}",
    }
    
    return send_template_email(
        'welcome',
        context,
        'Benvenuto su MyLabel!',
        [user.email]
    )

def send_booking_confirmation(booking):
    """Invia email di conferma prenotazione"""
    context = {
        'booking': booking,
        'artist': booking.artist,
        'associate': booking.associate,
    }
    
    # Email per l'artista
    send_template_email(
        'booking_confirmation_artist',
        context,
        'Prenotazione Confermata',
        [booking.artist.user.email]
    )
    
    # Email per l'associato
    send_template_email(
        'booking_confirmation_associate',
        context,
        'Nuova Prenotazione',
        [booking.associate.user.email]
    )

def send_new_message_notification(message):
    """Invia notifica per nuovo messaggio"""
    recipient = message.conversation.get_other_participant(message.sender)
    
    context = {
        'message': message,
        'sender': message.sender,
        'recipient': recipient,
    }
    
    return send_template_email(
        'new_message',
        context,
        f'Nuovo messaggio da {message.sender.get_full_name()}',
        [recipient.email]
    )
