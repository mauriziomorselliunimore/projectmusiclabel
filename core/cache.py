from django.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from functools import wraps
import hashlib
import json

def cache_key_from_args(*args, **kwargs):
    """Genera una chiave di cache unica dai parametri"""
    key = json.dumps((args, sorted(kwargs.items())), sort_keys=True)
    return hashlib.md5(key.encode()).hexdigest()

def cache_result(timeout=3600):
    """
    Decorator per cachare i risultati delle funzioni
    
    Usage:
    @cache_result(timeout=3600)
    def my_expensive_function(param1, param2):
        ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crea una chiave unica per questi argomenti
            cache_key = f"{func.__name__}:{cache_key_from_args(*args, **kwargs)}"
            
            # Prova a ottenere il risultato dalla cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Se non in cache, esegui la funzione
            result = func(*args, **kwargs)
            
            # Salva in cache per usi futuri
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

def invalidate_model_cache(sender, instance, **kwargs):
    """Invalida la cache quando un modello viene modificato"""
    model_name = sender.__name__.lower()
    cache.delete_pattern(f"{model_name}:*")

def setup_model_caching(model):
    """
    Configura il caching automatico per un modello
    
    Usage:
    setup_model_caching(Artist)
    """
    post_save.connect(invalidate_model_cache, sender=model)
    post_delete.connect(invalidate_model_cache, sender=model)

def cached_property(timeout=3600):
    """
    Decorator per cachare le property dei modelli
    
    Usage:
    @cached_property(timeout=3600)
    def expensive_property(self):
        ...
    """
    def decorator(func):
        @property
        @wraps(func)
        def wrapper(self):
            cache_key = f"{self.__class__.__name__}:{self.pk}:{func.__name__}"
            result = cache.get(cache_key)
            
            if result is None:
                result = func(self)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator
