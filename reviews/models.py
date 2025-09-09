from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    REVIEW_TYPES = [
        ('artist_to_associate', 'Da Artista a Professionista'),
        ('associate_to_artist', 'Da Professionista ad Artista'),
    ]

    """
    Tutto il codice delle recensioni è stato rimosso.
    """
"""
All review models have been removed as reviews are no longer needed.
"""
