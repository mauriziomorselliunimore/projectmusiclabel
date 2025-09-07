import time
import logging
from django.db import connection
from django.conf import settings
from django.middleware.security import SecurityMiddleware

logger = logging.getLogger('core.middleware')

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Inizia il timer
        start_time = time.time()
        
        # Conta le query prima della risposta
        n_queries_before = len(connection.queries)
        
        # Processa la richiesta
        response = self.get_response(request)
        
        # Se in modalità DEBUG o con monitoraggio attivo, registra le metriche
        if settings.DEBUG or getattr(settings, 'PERFORMANCE_MONITORING', False):
            # Calcola il tempo totale
            total_time = time.time() - start_time
            
            # Calcola il numero di query eseguite
            n_queries_after = len(connection.queries)
            n_queries = n_queries_after - n_queries_before
            
            # Log delle metriche
            logger.debug(f'''Performance metrics for {request.path}:
                Time: {total_time:.2f}s
                Queries: {n_queries}
                Status: {response.status_code}
            ''')
            
            # Se ci sono troppe query, logga un warning
            if n_queries > 100:
                logger.warning(f'High number of queries ({n_queries}) for {request.path}')
            
            # Se il tempo di risposta è alto, logga un warning
            if total_time > 1.0:  # più di 1 secondo
                logger.warning(f'Slow response ({total_time:.2f}s) for {request.path}')
                
            # Aggiungi le metriche agli header della risposta
            response['X-Response-Time'] = f'{total_time:.3f}'
            response['X-Queries-Count'] = str(n_queries)
        
        return response

class CustomSecurityMiddleware(SecurityMiddleware):
    def process_response(self, request, response):
        response = super().process_response(request, response)
        
        # Aggiunge headers di sicurezza
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Se in produzione e su HTTPS, aggiunge HSTS
        if request.is_secure() and not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            
        # Aggiunge Content Security Policy in produzione
        if not settings.DEBUG:
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
                "font-src 'self' https://cdn.jsdelivr.net; "
                "connect-src 'self' wss: https:; "
                "media-src 'self' https:; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none';"
            )
            response['Content-Security-Policy'] = csp
            
        return response

class APIMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Processa solo le richieste API
        if not request.path.startswith('/api/'):
            return self.get_response(request)
            
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        # Log delle metriche API
        logger.info(f'''API Request:
            Path: {request.path}
            Method: {request.method}
            Status: {response.status_code}
            Duration: {duration:.3f}s
            User: {request.user}
        ''')
        
        return response
