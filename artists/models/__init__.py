from django.db import models
from .models import Artist, Demo
from .collaboration import CollaborationProposal

# Espone i modelli al livello superiore
__all__ = ['Artist', 'Demo', 'CollaborationProposal']
