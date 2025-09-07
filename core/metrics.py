"""
Provides metrics and monitoring functions for the application.
"""
import time
import logging
from functools import wraps
from django.db import connection
from django.conf import settings

logger = logging.getLogger('core.metrics')

def query_debugger(func):
    """
    Decorator per tracciare le query del database.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries = False
        if settings.DEBUG:
            reset_queries = True
            start_queries = len(connection.queries)

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        if reset_queries:
            end_queries = len(connection.queries)
            queries = end_queries - start_queries
            logger.debug(f'''
                Funzione: {func.__name__}
                Numero di query: {queries}
                Tempo finito: {(end - start):.2f}s
            ''')

        return result
    return wrapper

class MetricsCollector:
    """
    Raccoglie metriche di performance per views e funzioni.
    """
    def __init__(self):
        self.metrics = {}

    def record_metric(self, category, name, value, tags=None):
        """
        Registra una metrica con categoria, nome e valore.
        """
        if tags is None:
            tags = {}

        key = f"{category}.{name}"
        if key not in self.metrics:
            self.metrics[key] = []

        self.metrics[key].append({
            'value': value,
            'timestamp': time.time(),
            'tags': tags
        })

        # Log della metrica
        logger.info(f"Metric: {key}={value} {tags}")

    def get_metrics(self, category=None):
        """
        Recupera metriche, opzionalmente filtrate per categoria.
        """
        if category:
            return {k: v for k, v in self.metrics.items() if k.startswith(f"{category}.")}
        return self.metrics

    def clear_metrics(self):
        """
        Cancella tutte le metriche salvate.
        """
        self.metrics = {}

# Istanza globale del collector
metrics = MetricsCollector()

def monitor_performance(category):
    """
    Decorator per monitorare performance di funzioni e views.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_queries = len(connection.queries)

            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                raise e
            finally:
                end_time = time.time()
                duration = end_time - start_time
                queries = len(connection.queries) - start_queries

                # Registra metriche
                metrics.record_metric(
                    category=category,
                    name='duration',
                    value=duration,
                    tags={'function': func.__name__, 'success': success}
                )
                metrics.record_metric(
                    category=category,
                    name='queries',
                    value=queries,
                    tags={'function': func.__name__}
                )

            return result
        return wrapper
    return decorator
