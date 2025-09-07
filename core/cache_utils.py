import logging
from django.conf import settings
from functools import wraps
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from reviews.cache import get_user_ratings

# Configurazione logger
logger = logging.getLogger(__name__)

def cache_profile_page(view_func):
    """
    Decorator per cachare le pagine profilo con timeout variabile
    basato sul tipo di utente.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Cache più lunga per utenti non autenticati
            decorator = cache_page(settings.CACHE_MIDDLEWARE_SECONDS * 2)
        else:
            # Cache più breve per utenti autenticati
            decorator = cache_page(settings.CACHE_MIDDLEWARE_SECONDS)
        
        # Varia la cache in base al cookie di sessione
        return method_decorator(decorator)(vary_on_cookie(view_func))(request, *args, **kwargs)
        
    return _wrapped_view

def cache_safe_method(timeout=None):
    """
    Decorator per cachare solo metodi GET sicuri.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != 'GET':
                return view_func(request, *args, **kwargs)
            
            cache_timeout = timeout or settings.CACHE_MIDDLEWARE_SECONDS
            decorator = cache_page(cache_timeout)
            return decorator(view_func)(request, *args, **kwargs)
            
        return _wrapped_view
    return decorator

def get_cached_ratings(user_id, review_type):
    """
    Recupera le valutazioni dalla cache o dal database.
    """
    try:
        return get_user_ratings(user_id, review_type)
    except Exception as e:
        logger.error(f'Error getting ratings for user {user_id}: {str(e)}')
        return None

def invalidate_profile_cache(user_id):
    """
    Invalida la cache del profilo utente.
    """
    cache_keys = [
        f'profile_page_{user_id}',
        f'user_ratings_{user_id}_artist_to_associate',
        f'user_ratings_{user_id}_associate_to_artist'
    ]
    
    for key in cache_keys:
        try:
            cache.delete(key)
        except Exception as e:
            logger.error(f'Error invalidating cache key {key}: {str(e)}')
