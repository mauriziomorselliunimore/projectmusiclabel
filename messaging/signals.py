from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_save, sender=User)
def send_welcome_message(sender, instance, created, **kwargs):
    """Invia un messaggio di benvenuto quando viene creato un nuovo utente"""
    if created:  # Solo per nuovi utenti
        call_command('send_welcome_messages')
