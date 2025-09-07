from django.core.cache import cache
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from reviews.models import Review

def get_cache_key(user_id, review_type):
    """Genera una chiave cache per le medie delle recensioni di un utente"""
    return f'user_ratings_{user_id}_{review_type}'

def get_user_ratings(user_id, review_type):
    """
    Recupera le medie delle recensioni per un utente, usando la cache.
    """
    cache_key = get_cache_key(user_id, review_type)
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # Se non in cache, calcola le medie
        reviews = Review.objects.filter(reviewed_id=user_id, review_type=review_type)
        
        if review_type == 'artist_to_associate':
            ratings = reviews.aggregate(
                avg_professionalism=Avg('professionalism'),
                avg_communication=Avg('communication'),
                avg_value=Avg('value'),
                avg_rating=Avg('rating')
            )
        else:  # associate_to_artist
            ratings = reviews.aggregate(
                avg_reliability=Avg('reliability'),
                avg_preparation=Avg('preparation'),
                avg_collaboration=Avg('collaboration'),
                avg_rating=Avg('rating')
            )
        
        # Salva in cache per future richieste
        cache.set(cache_key, ratings, settings.RATINGS_CACHE_TIMEOUT)
        return ratings
    
    return cached_data

@receiver(post_save, sender=Review)
def invalidate_ratings_cache(sender, instance, **kwargs):
    """Invalida la cache quando una recensione viene creata o modificata"""
    cache_key = get_cache_key(instance.reviewed_id, instance.review_type)
    cache.delete(cache_key)

@receiver(post_delete, sender=Review)
def invalidate_ratings_cache_on_delete(sender, instance, **kwargs):
    """Invalida la cache quando una recensione viene eliminata"""
    cache_key = get_cache_key(instance.reviewed_id, instance.review_type)
    cache.delete(cache_key)
