from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def star_range(value):
    """
    Converte un valore numerico in un range per visualizzare le stelle piene.
    """
    try:
        return range(int(float(value or 0)))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def empty_star_range(value):
    """
    Restituisce il range per le stelle vuote (5 - stelle piene).
    """
    try:
        filled = int(float(value or 0))
        return range(5 - filled)
    except (ValueError, TypeError):
        return range(5)

@register.inclusion_tag('reviews/includes/professional_ratings.html')
def show_professional_ratings(reviews):
    """Mostra le valutazioni professionali medie"""
    avg_ratings = reviews.aggregate(
        avg_professionalism=Avg('professionalism'),
        avg_communication=Avg('communication'),
        avg_value=Avg('value')
    )
    
    return {
        'avg_professionalism': avg_ratings['avg_professionalism'] or 0,
        'avg_communication': avg_ratings['avg_communication'] or 0,
        'avg_value': avg_ratings['avg_value'] or 0,
    }

@register.inclusion_tag('reviews/includes/artist_ratings.html')
def show_artist_ratings(reviews):
    """Mostra le valutazioni degli artisti medie"""
    avg_ratings = reviews.aggregate(
        avg_reliability=Avg('reliability'),
        avg_preparation=Avg('preparation'),
        avg_collaboration=Avg('collaboration')
    )
    
    return {
        'avg_reliability': avg_ratings['avg_reliability'] or 0,
        'avg_preparation': avg_ratings['avg_preparation'] or 0,
        'avg_collaboration': avg_ratings['avg_collaboration'] or 0,
    }
