# core/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin user if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@mylabel.com',
                password='admin123',
                first_name='Admin',
                last_name='MyLabel'
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Superuser "admin" created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Superuser "admin" already exists')
            )