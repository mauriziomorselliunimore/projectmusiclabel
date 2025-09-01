from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """Converte un URL YouTube in un URL per l'embed"""
    if not url:
        return ''
    
    parsed = urlparse(url)
    if 'youtu.be' in parsed.netloc:
        # Formato youtu.be
        video_id = parsed.path[1:]
    else:
        # Formato youtube.com
        query = parse_qs(parsed.query)
        video_id = query.get('v', [''])[0]
    
    return f'https://www.youtube.com/embed/{video_id}'

@register.filter
def spotify_embed_url(url):
    """Converte un URL Spotify in un URL per l'embed"""
    if not url:
        return ''
    
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    
    if len(path_parts) < 3:
        return url
    
    # Determina il tipo (track, album, artist)
    content_type = path_parts[1]
    content_id = path_parts[2]
    
    return f'https://open.spotify.com/embed/{content_type}/{content_id}'
