from django.db import models
from .models import Artist, Demo
from .collaboration import CollaborationProposal
from .constants import MUSIC_GENRES, ARTIST_ICONS

# Espone i modelli e le costanti al livello superiore
__all__ = [
    'Artist', 'Demo', 'CollaborationProposal',
    'MUSIC_GENRES', 'ARTIST_ICONS'
]
