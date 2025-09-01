# core/management/commands/create_simple_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create simple admin user (admin/admin) if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Superuser "admin" (password: admin) created successfully!')
            )
        else:
            # Se l'admin esiste già, aggiorna la sua password
            admin = User.objects.get(username='admin')
            admin.set_password('admin')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(
                self.style.SUCCESS('✅ Existing admin password updated to "admin"')
            )
