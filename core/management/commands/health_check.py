from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import os
import psutil
import redis
import logging
from django.contrib.auth.models import User
from reviews.models import Review
from artists.models import Artist
from associates.models import Associate

logger = logging.getLogger('core.management')

class Command(BaseCommand):
    help = 'Verifica lo stato del sistema e genera un report'

    def add_arguments(self, parser):
        parser.add_argument(
            '--full',
            action='store_true',
            help='Esegue anche i test più pesanti',
        )

    def check_database(self):
        """Verifica la connessione al database e le performance"""
        self.stdout.write('Verifico database...')
        
        try:
            # Test connessione
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
            
            # Stats
            stats = {
                'users': User.objects.count(),
                'artists': Artist.objects.count(),
                'associates': Associate.objects.count(),
                'reviews': Review.objects.count(),
            }
            
            self.stdout.write(self.style.SUCCESS(
                f'Database OK - Users: {stats["users"]}, '
                f'Artists: {stats["artists"]}, '
                f'Associates: {stats["associates"]}, '
                f'Reviews: {stats["reviews"]}'
            ))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database error: {str(e)}'))
            return False

    def check_cache(self):
        """Verifica la connessione Redis e le performance"""
        self.stdout.write('Verifico cache...')
        
        try:
            # Test Redis
            cache.set('health_check', 'ok')
            result = cache.get('health_check')
            cache.delete('health_check')
            
            if result != 'ok':
                raise Exception('Cache test failed')
                
            # Get Redis info
            redis_client = redis.from_url(settings.CACHES['default']['LOCATION'])
            info = redis_client.info()
            
            self.stdout.write(self.style.SUCCESS(
                f'Cache OK - Used memory: {info["used_memory_human"]}, '
                f'Connected clients: {info["connected_clients"]}'
            ))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Cache error: {str(e)}'))
            return False

    def check_storage(self):
        """Verifica lo spazio su disco e i permessi"""
        self.stdout.write('Verifico storage...')
        
        try:
            # Check disk space
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024 * 1024 * 1024)
            
            # Check media directory
            media_path = settings.MEDIA_ROOT
            static_path = settings.STATIC_ROOT
            
            if not os.path.exists(media_path):
                os.makedirs(media_path)
            if not os.path.exists(static_path):
                os.makedirs(static_path)
                
            # Test write permissions
            test_file = os.path.join(media_path, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            self.stdout.write(self.style.SUCCESS(
                f'Storage OK - Free space: {free_gb:.1f}GB'
            ))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Storage error: {str(e)}'))
            return False

    def check_security(self):
        """Verifica le impostazioni di sicurezza"""
        self.stdout.write('Verifico sicurezza...')
        
        checks = {
            'DEBUG': not settings.DEBUG,
            'SECRET_KEY': len(settings.SECRET_KEY) >= 50,
            'ALLOWED_HOSTS': len(settings.ALLOWED_HOSTS) > 0,
            'SECURE_SSL_REDIRECT': getattr(settings, 'SECURE_SSL_REDIRECT', False),
            'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
            'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
        }
        
        failed = [k for k, v in checks.items() if not v]
        
        if failed:
            self.stdout.write(self.style.WARNING(
                f'Security warnings: {", ".join(failed)}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('Security OK'))
            
        return len(failed) == 0

    def check_system(self):
        """Verifica le risorse di sistema"""
        self.stdout.write('Verifico sistema...')
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            self.stdout.write(self.style.SUCCESS(
                f'System OK - CPU: {cpu_percent}%, '
                f'Memory: {memory_percent}%'
            ))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'System error: {str(e)}'))
            return False

    def handle(self, *args, **options):
        self.stdout.write('Inizia health check...\n')
        
        results = {
            'database': self.check_database(),
            'cache': self.check_cache(),
            'storage': self.check_storage(),
            'security': self.check_security(),
            'system': self.check_system(),
        }
        
        if options['full']:
            # Aggiungi test aggiuntivi qui
            pass
        
        # Report finale
        self.stdout.write('\nReport Finale:')
        all_ok = all(results.values())
        
        for check, result in results.items():
            status = 'OK' if result else 'FAIL'
            style = self.style.SUCCESS if result else self.style.ERROR
            self.stdout.write(f'{check:.<20}{style(status)}')
        
        if all_ok:
            self.stdout.write(self.style.SUCCESS('\nTutti i check sono passati!'))
        else:
            self.stdout.write(self.style.ERROR('\nAlcuni check sono falliti.'))
