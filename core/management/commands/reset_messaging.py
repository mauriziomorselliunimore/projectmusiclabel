from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset messaging tables'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                cursor.execute("DROP TABLE IF EXISTS messaging_conversation CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS messaging_message CASCADE;") 
                cursor.execute("DROP TABLE IF EXISTS messaging_notification CASCADE;")
                self.stdout.write('✅ Messaging tables dropped')
            except Exception as e:
                self.stdout.write(f'⚠️ {e}')