from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup messaging system with migrations'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Setting up messaging system...')
        
        try:
            # Check if tables exist
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_name = 'messaging_conversation'
                """)
                tables_exist = cursor.fetchone()[0] > 0
            
            if not tables_exist:
                self.stdout.write('📊 Creating messaging tables...')
                call_command('migrate', 'messaging', verbosity=2)
                self.stdout.write('✅ Messaging tables created!')
            else:
                self.stdout.write('✅ Messaging tables already exist')
                
        except Exception as e:
            self.stdout.write(f'❌ Error: {e}')