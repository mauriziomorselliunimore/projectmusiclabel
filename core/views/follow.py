from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from artists.models import Artist
from associates.models import Associate
from core.models import Follow

@login_required
def toggle_follow(request, content_type_id, object_id):
    """Vista per seguire/smettere di seguire un artista o un associato"""
    content_type = get_object_or_404(ContentType, id=content_type_id)
    
    # Verifica che il content type sia valido
    if content_type.model_class() not in [Artist, Associate]:
        return JsonResponse({'error': 'Tipo non valido'}, status=400)
    
    # Ottieni l'oggetto da seguire
    try:
        obj = content_type.get_object_for_this_type(id=object_id)
    except:
        return JsonResponse({'error': 'Oggetto non trovato'}, status=404)
    
    # Non permettere di seguire se stessi
    if hasattr(request.user, 'artist') and request.user.artist == obj:
        return JsonResponse({'error': 'Non puoi seguire te stesso'}, status=400)
    if hasattr(request.user, 'associate') and request.user.associate == obj:
        return JsonResponse({'error': 'Non puoi seguire te stesso'}, status=400)
    
    # Trova o crea il follow
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        content_type=content_type,
        object_id=object_id
    )
    
    # Se esisteva già, rimuovilo
    if not created:
        follow.delete()
        is_following = False
        message = f"Non segui più {obj}"
    else:
        is_following = True
        message = f"Ora segui {obj}"
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'message': message,
            'followers_count': Follow.objects.filter(
                content_type=content_type,
                object_id=object_id
            ).count()
        })
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', '/'))
