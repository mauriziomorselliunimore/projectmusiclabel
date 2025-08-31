from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from messaging.models import Conversation, Message
from django.conf import settings

class Command(BaseCommand):
    help = 'Invia un messaggio di benvenuto a tutti gli utenti che non ne hanno ancora ricevuto uno'

    def get_welcome_message(self, user):
        """Personalizza il messaggio in base al tipo di utente"""
        if hasattr(user, 'profile'):
            if user.profile.user_type == 'artist':
                return {
                    'subject': 'Benvenuto su MyLabel! 🎵',
                    'content': f"""Ciao {user.get_full_name() or user.username}!

Benvenuto nella nostra piattaforma musicale. Come artista, qui potrai:
• Caricare le tue demo
• Prenotare sessioni con i nostri professionisti
• Collaborare con altri artisti

Se hai bisogno di aiuto o hai domande, non esitare a rispondere a questo messaggio.

Il team MyLabel 🎼"""
                }
            elif user.profile.user_type == 'associate':
                return {
                    'subject': 'Benvenuto su MyLabel! 🎸',
                    'content': f"""Ciao {user.get_full_name() or user.username}!

Benvenuto nella nostra piattaforma musicale. Come professionista, qui potrai:
• Gestire le tue disponibilità
• Ricevere prenotazioni
• Mostrare il tuo portfolio

Se hai bisogno di aiuto o hai domande, non esitare a rispondere a questo messaggio.

Il team MyLabel 🎼"""
                }
        
        # Messaggio generico se non riusciamo a determinare il tipo di utente
        return {
            'subject': 'Benvenuto su MyLabel! 🎼',
            'content': f"""Ciao {user.get_full_name() or user.username}!

Benvenuto nella nostra piattaforma musicale. Qui potrai:
• Interagire con artisti e professionisti
• Partecipare alla nostra community
• Scoprire nuove opportunità

Se hai bisogno di aiuto o hai domande, non esitare a rispondere a questo messaggio.

Il team MyLabel 🎼"""
        }

    def handle(self, *args, **kwargs):
        # Ottieni l'utente admin (assumiamo sia il primo superuser)
        try:
            admin = User.objects.filter(is_superuser=True).first()
            if not admin:
                self.stdout.write(self.style.ERROR('Nessun admin trovato nel sistema'))
                return
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nessun admin trovato nel sistema'))
            return

        # Trova tutti gli utenti che non hanno conversazioni con l'admin
        users_without_welcome = User.objects.exclude(
            id=admin.id
        ).exclude(
            conversations_as_participant_1__participant_2=admin
        ).exclude(
            conversations_as_participant_2__participant_1=admin
        )

        count = 0
        for user in users_without_welcome:
            # Crea una nuova conversazione
            conversation = Conversation.objects.create(
                participant_1=admin,
                participant_2=user
            )

            # Ottieni il messaggio personalizzato
            welcome_message = self.get_welcome_message(user)

            # Crea il messaggio di benvenuto
            Message.objects.create(
                conversation=conversation,
                sender=admin,
                recipient=user,
                subject=welcome_message['subject'],
                message=welcome_message['content'],
                message_type='general'
            )
            count += 1

        if count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Inviati {count} messaggi di benvenuto con successo')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Nessun nuovo messaggio di benvenuto da inviare')
            )
