from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_template_email(template_name, context, subject, recipient_list, from_email=None):
    """
    Invia una email usando un template HTML
    
    Args:
        template_name (str): Nome del template email (senza estensione)
        context (dict): Contesto per il template
        subject (str): Oggetto dell'email
        recipient_list (list): Lista di indirizzi email destinatari
        from_email (str, optional): Email mittente. Default None (usa DEFAULT_FROM_EMAIL)
    """
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    
    # Renderizza il template HTML
    html_content = render_to_string(f'emails/{template_name}.html', context)
    text_content = strip_tags(html_content)
    
    # Crea il messaggio
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient_list
    )
    msg.attach_alternative(html_content, "text/html")
    
    # Invia
    return msg.send()

def send_welcome_email(user):
    """Invia email di benvenuto a un nuovo utente"""
    context = {
        'user': user,
        'login_url': settings.LOGIN_URL,
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
