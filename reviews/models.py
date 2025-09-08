from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    REVIEW_TYPES = [
        ('artist_to_associate', 'Da Artista a Professionista'),
        ('associate_to_artist', 'Da Professionista ad Artista'),
    ]

    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    reviewed = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    review_type = models.CharField(
        max_length=20,
        choices=REVIEW_TYPES,
        help_text=_('Tipo di recensione')
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Valutazione da 1 a 5 stelle')
    )
    
    title = models.CharField(
        max_length=100,
        help_text=_('Titolo breve della recensione')
    )
    
    content = models.TextField(
        max_length=1000,
        help_text=_('Testo della recensione')
    )
    
    # Campi specifici per recensioni da artista a professionista
    professionalism = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione della professionalità')
    )
    communication = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione della comunicazione')
    )
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione del rapporto qualità/prezzo')
    )
    
    # Campi specifici per recensioni da professionista ad artista
    reliability = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione dell\'affidabilità')
    )
    preparation = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione della preparazione')
    )
    collaboration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text=_('Valutazione della capacità di collaborazione')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['reviewer', 'reviewed']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Recensione di {self.reviewer} per {self.reviewed}"
        
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Verifica che il recensore sia del tipo corretto per il tipo di recensione
        if self.review_type == 'artist_to_associate':
            if not hasattr(self.reviewer, 'artist'):
                raise ValidationError('Solo gli artisti possono lasciare questo tipo di recensione')
            if not hasattr(self.reviewed, 'associate'):
                raise ValidationError('Questa recensione può essere lasciata solo a professionisti')
        
        elif self.review_type == 'associate_to_artist':
            if not hasattr(self.reviewer, 'associate'):
                raise ValidationError('Solo i professionisti possono lasciare questo tipo di recensione')
            if not hasattr(self.reviewed, 'artist'):
                raise ValidationError('Questa recensione può essere lasciata solo ad artisti')
    
    def get_average_rating(self):
        """Calcola la media delle valutazioni specifiche in base al tipo di recensione"""
        if self.review_type == 'artist_to_associate':
            ratings = [self.professionalism, self.communication, self.value]
        else:
            ratings = [self.reliability, self.preparation, self.collaboration]
            
        valid_ratings = [r for r in ratings if r is not None]
        return sum(valid_ratings) / len(valid_ratings) if valid_ratings else self.rating
"""
All review models have been removed as reviews are no longer needed.
"""
