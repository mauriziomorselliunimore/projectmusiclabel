# settings/cache.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'RETRY_ON_TIMEOUT': True,
        },
    }
}

# Cache settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Cache timeouts (in seconds)
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 minuti
RATINGS_CACHE_TIMEOUT = 60 * 60 * 24  # 24 ore
USER_PROFILE_CACHE_TIMEOUT = 60 * 60  # 1 ora

# Cache middleware
if not DEBUG:
    MIDDLEWARE = ['django.middleware.cache.UpdateCacheMiddleware'] + MIDDLEWARE
    MIDDLEWARE += ['django.middleware.cache.FetchFromCacheMiddleware']

# Cache versioning
CACHE_VERSION = 1
CACHE_KEY_PREFIX = 'v1'
