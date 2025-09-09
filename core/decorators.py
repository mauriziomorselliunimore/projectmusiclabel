from functools import wraps
from django.core.cache import cache
from django.http import HttpResponseForbidden
import time

def ratelimit(key='ip', rate='5/15m', block=True):
    """
    Rate limiting decorator
    :param key: 'ip' o 'user'
    :param rate: formato 'numero/periodo' es. '5/15m' per 5 tentativi ogni 15 minuti
    :param block: se True, blocca le richieste eccessive
    """
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            # Parsing del rate
            count, period = rate.split('/')
            count = int(count)
            period_seconds = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
            period_mult = period_seconds[period[-1]]
            period = int(period[:-1]) * period_mult

            # Generazione della chiave cache
            if key == 'ip':
                cache_key = f'ratelimit_{func.__name__}_{request.META.get("REMOTE_ADDR")}'
            elif key == 'user' and request.user.is_authenticated:
                cache_key = f'ratelimit_{func.__name__}_{request.user.id}'
            else:
                cache_key = f'ratelimit_{func.__name__}_anonymous'

            # Controllo del rate limit
            requests = cache.get(cache_key, [])
            now = time.time()
            
            # Rimuovi i timestamp più vecchi del periodo
            requests = [r for r in requests if r > (now - period)]
            
            if len(requests) >= count:
                if block:
                    return HttpResponseForbidden(
                        'Troppi tentativi. Riprova più tardi.'
                    )
            
            # Aggiungi il timestamp corrente e aggiorna la cache
            requests.append(now)
            cache.set(cache_key, requests, period)
            
            return func(request, *args, **kwargs)
        return wrapped
    return decorator
