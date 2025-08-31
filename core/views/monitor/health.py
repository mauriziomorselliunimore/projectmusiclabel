from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from redis.exceptions import RedisError
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Verifica lo stato del sistema
    """
    health = {
        'status': 'healthy',
        'components': {
            'database': True,
            'cache': True
        },
        'details': {}
    }

    # Controllo Database
    try:
        connections['default'].cursor()
    except OperationalError as e:
        health['status'] = 'unhealthy'
        health['components']['database'] = False
        health['details']['database'] = str(e)
        logger.error(f"Database health check failed: {e}")

    # Controllo Cache
    try:
        cache.set('health_check', 'ok', 1)
        if cache.get('health_check') != 'ok':
            raise Exception("Cache test failed")
    except (RedisError, Exception) as e:
        health['status'] = 'unhealthy'
        health['components']['cache'] = False
        health['details']['cache'] = str(e)
        logger.error(f"Cache health check failed: {e}")

    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)
