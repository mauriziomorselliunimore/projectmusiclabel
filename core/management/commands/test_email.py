from django.core.mail import send_mail
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test invio email con SendGrid'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='Test Email da MyLabel',
                message='Se vedi questa email, la configurazione SendGrid funziona correttamente!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.VERIFIED_SENDER_EMAIL],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS('Email di test inviata con successo!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Errore invio email: {str(e)}')
            )
