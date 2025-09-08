
from django.db import models


from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from artists.models import Artist
from associates.models import Associate

class Booking(models.Model):
    """Sistema prenotazione sessioni studio con prevenzione conflitti"""
    BOOKING_STATUS = [
        ('pending', 'In Attesa'),
        ('confirmed', 'Confermato'),
        ('completed', 'Completato'),
        ('cancelled', 'Cancellato'),
        ('counter_proposed', 'Controproposta Inviata'),
    ]
    
    COUNTER_PROPOSAL_STATUS = [
        ('pending', 'In Attesa'),
        ('accepted', 'Accettata'),
        ('rejected', 'Rifiutata'),
    ]
    
    BOOKING_TYPES = [
        ('recording', 'Sessione Registrazione'),
        ('mixing', 'Mixing'),
        ('mastering', 'Mastering'),
        ('production', 'Produzione'),
        ('lesson', 'Lezione'),
        ('consultation', 'Consulenza'),
        ('other', 'Altro'),
    ]
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='bookings')
    associate = models.ForeignKey(Associate, on_delete=models.CASCADE, related_name='bookings')
    
    # Dettagli sessione
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES, default='recording')
    session_date = models.DateTimeField()
    duration_hours = models.PositiveIntegerField(default=2, help_text="Durata in ore")
    
    # Info aggiuntive
    location = models.CharField(max_length=200, blank=True, help_text="Studio o località")
    notes = models.TextField(max_length=1000, blank=True, help_text="Note specifiche per la sessione")
    special_requirements = models.TextField(max_length=500, blank=True, help_text="Richieste speciali")
    
    # Status e pagamento
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-session_date']
        # Previeni conflitti: stesso associato non può avere 2 booking sovrapposti
        constraints = [
            models.CheckConstraint(
                check=models.Q(duration_hours__gte=1) & models.Q(duration_hours__lte=12),
                name='valid_duration'
            )
        ]
    
    def __str__(self):
        return f"{self.artist.stage_name} → {self.associate.user.get_full_name()} - {self.session_date.strftime('%d/%m/%Y %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('booking:detail', kwargs={'pk': self.pk})
    
    def clean(self):
        """Validazione business rules"""
        super().clean()
        
        # Non permettere booking nel passato
        if self.session_date and self.session_date <= timezone.now():
            raise ValidationError({'session_date': 'Non puoi prenotare nel passato!'})
        # Verifica conflitti orari per l'associato solo se associato è presente
        if self.session_date and self.associate:
            end_time = self.session_date + timedelta(hours=self.duration_hours)
            conflicting_bookings = Booking.objects.filter(
                associate=self.associate,
                status__in=['pending', 'confirmed'],
                session_date__lt=end_time,
                session_date__gte=self.session_date - timedelta(hours=12)
            ).exclude(pk=self.pk)
            for booking in conflicting_bookings:
                booking_end = booking.session_date + timedelta(hours=booking.duration_hours)
                if (self.session_date < booking_end and 
                    end_time > booking.session_date):
                    raise ValidationError({
                        'session_date': f'Conflitto orario con booking esistente: {booking}'
                    })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Calcola costo automaticamente se possibile
        if not self.total_cost and self.associate.hourly_rate:
            self.total_cost = self.associate.hourly_rate * self.duration_hours
            
        super().save(*args, **kwargs)
    
    @property
    def end_time(self):
        return self.session_date + timedelta(hours=self.duration_hours)
    
    @property
    def is_upcoming(self):
        return self.session_date > timezone.now()
    
    @property
    def can_be_cancelled(self):
        # Può essere cancellato fino a 24h prima
        return self.is_upcoming and (self.session_date - timezone.now()).total_seconds() > 86400


class Availability(models.Model):
    """Disponibilità associate per calendario booking"""
    DAYS_OF_WEEK = [
        (0, 'Lunedì'), (1, 'Martedì'), (2, 'Mercoledì'), 
        (3, 'Giovedì'), (4, 'Venerdì'), (5, 'Sabato'), (6, 'Domenica')
    ]
    
    associate = models.ForeignKey(Associate, on_delete=models.CASCADE, related_name='availability_slots')
    
    # Disponibilità ricorrente
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Disponibilità specifica (override)
    is_recurring = models.BooleanField(default=True)
    specific_date = models.DateField(null=True, blank=True, help_text="Per disponibilità in date specifiche")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.is_recurring and self.specific_date:
            # Se è una disponibilità specifica, impostiamo il giorno della settimana in base alla data
            self.day_of_week = self.specific_date.weekday()
        elif self.is_recurring:
            # Se è ricorrente, assicuriamoci che specific_date sia None
            self.specific_date = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['associate', 'day_of_week', 'start_time', 'specific_date']
    
    def clean(self):
        if self.is_recurring and not self.day_of_week:
            raise ValidationError({
                'day_of_week': 'Il giorno della settimana è richiesto per le disponibilità ricorrenti'
            })
        if not self.is_recurring and not self.specific_date:
            raise ValidationError({
                'specific_date': 'La data specifica è richiesta per le disponibilità non ricorrenti'
            })
    
    def __str__(self):
        if self.specific_date:
            return f"{self.associate.user.get_full_name()} - {self.specific_date} {self.start_time}-{self.end_time}"
        
        day_name = dict(self.DAYS_OF_WEEK)[self.day_of_week]
        return f"{self.associate.user.get_full_name()} - {day_name} {self.start_time}-{self.end_time}"
    
    def clean(self):
        super().clean()
        if self.start_time >= self.end_time:
            raise ValidationError({'end_time': 'L\'ora di fine deve essere dopo l\'inizio'})