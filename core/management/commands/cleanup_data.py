from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from messaging.models import Message, Conversation
from booking.models import Booking

class Command(BaseCommand):
    help = 'Pulisce i dati vecchi dal database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Numero di giorni dopo cui considerare i dati come vecchi'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra cosa verrebbe eliminato senza effettuare modifiche'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Messaggi vecchi
        old_messages = Message.objects.filter(
            Q(created_at__lt=cutoff_date),
            Q(is_archived=True) | Q(is_read=True)
        )
        
        # Prenotazioni completate vecchie
        old_bookings = Booking.objects.filter(
            status='completed',
            created_at__lt=cutoff_date
        )
        
        # Conversazioni vuote
        empty_conversations = Conversation.objects.filter(
            messages__isnull=True,
            created_at__lt=cutoff_date
        )
        
        if dry_run:
            self.stdout.write(f"Verrebbero eliminati:")
            self.stdout.write(f"- {old_messages.count()} messaggi vecchi")
            self.stdout.write(f"- {old_bookings.count()} prenotazioni vecchie")
            self.stdout.write(f"- {empty_conversations.count()} conversazioni vuote")
        else:
            old_messages.delete()
            old_bookings.delete()
            empty_conversations.delete()
            
            self.stdout.write(self.style.SUCCESS(
                f"Pulizia completata! Eliminati elementi più vecchi di {days} giorni"
            ))
