from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import timedelta

ASSOCIATE_ICONS = [
    ('bi-person-circle', 'Persona'),
    ('bi-gear', 'Ingranaggio'),
    ('bi-tools', 'Strumenti'),
    ('bi-sliders', 'Mixer'),
    ('bi-music-note-list', 'Spartito'),
    ('bi-camera', 'Fotocamera'),
    ('bi-film', 'Video'),
    ('bi-palette', 'Tavolozza'),
    ('bi-briefcase', 'Valigetta'),
    ('bi-headset', 'Cuffie'),
    ('bi-megaphone', 'Megafono'),
]

SKILLS = [
    ('sound-engineer', 'Fonico'),
    ('producer', 'Produttore'),
    ('mixing', 'Mixing'),
    ('mastering', 'Mastering'),
    ('session-musician', 'Musicista Session'),
    ('drummer', 'Batterista'),
    ('guitarist', 'Chitarrista'),
    ('bassist', 'Bassista'),
    ('keyboardist', 'Tastierista'),
    ('vocalist', 'Vocalist'),
    ('songwriter', 'Songwriter'),
    ('arranger', 'Arrangiatore'),
    ('graphic-designer', 'Grafico'),
    ('video-editor', 'Video Editor'),
    ('photographer', 'Fotografo'),
    ('manager', 'Manager'),
    ('booking-agent', 'Booking Agent'),
    ('other', 'Altro'),
]

EXPERIENCE_LEVELS = [
    ('beginner', 'Principiante'),
    ('intermediate', 'Intermedio'),
    ('advanced', 'Avanzato'),
    ('professional', 'Professionale'),
]

class Associate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, help_text="Specializzazione principale")
    profile_icon = models.CharField(max_length=50, choices=ASSOCIATE_ICONS, default='bi-tools', null=True, blank=True, help_text="Icona del profilo")
    profile_icon_color = models.CharField(max_length=7, default='#10b981', null=True, blank=True, help_text="Colore dell'icona (es. #10b981)")
    skills = models.CharField(max_length=300, help_text="Competenze separate da virgola")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='intermediate')
    
    # Business Info
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Tariffa oraria in €")
    availability = models.CharField(max_length=200, blank=True, help_text="Disponibilità oraria")
    
    # Profile Info
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Portfolio
    portfolio_description = models.TextField(max_length=500, blank=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    
    # Settings
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"
    
    def get_absolute_url(self):
        return reverse('associates:detail', kwargs={'pk': self.pk})
    
    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]
    
    def get_rate_display(self):
        if self.hourly_rate:
            return f"€{self.hourly_rate}/ora"
        return "Tariffa da concordare"

class PortfolioItem(models.Model):
    associate = models.ForeignKey(Associate, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    
    # Data di completamento del progetto
    completion_date = models.DateField(null=True, blank=True)
    
    # URL esterni invece di file upload
    external_image_url = models.URLField(blank=True, help_text="Link a immagine (Imgur, Google Drive, etc.)")
    external_audio_url = models.URLField(blank=True, help_text="Link audio (SoundCloud, YouTube, etc.)")
    external_url = models.URLField(blank=True, help_text="Link esterno principale (YouTube, SoundCloud, sito web, etc.)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.associate.user.get_full_name()} - {self.title}"
    
    def get_primary_url(self):
        """Restituisce l'URL principale da mostrare"""
        return self.external_url or self.external_audio_url or self.external_image_url
    
    def get_platform(self):
        """Identifica la piattaforma dal URL principale"""
        url = self.get_primary_url()
        if not url:
            return None
            
        url = url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'soundcloud.com' in url:
            return 'soundcloud'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'drive'
        elif 'imgur.com' in url:
            return 'imgur'
        else:
            return 'website'

class Availability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lunedì'),
        (1, 'Martedì'),
        (2, 'Mercoledì'),
        (3, 'Giovedì'),
        (4, 'Venerdì'),
        (5, 'Sabato'),
        (6, 'Domenica'),
    ]

    associate = models.ForeignKey(Associate, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(help_text="Data di disponibilità")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, help_text="Giorno della settimana", default=0)  # Lunedì come default
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False, help_text="Se true, questa disponibilità si ripete ogni settimana")
    recurrence_end_date = models.DateField(null=True, blank=True, help_text="Data fine ricorrenza")
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Availabilities"
        ordering = ['date', 'start_time']
        unique_together = ['associate', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.associate} - {self.date.strftime('%d/%m/%Y')} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    def get_recurring_dates(self, end_date=None):
        """Restituisce tutte le date in cui questo slot si ripete"""
        if not self.is_recurring:
            return [self.date]
        
        end = end_date or self.recurrence_end_date or (self.date + timedelta(days=90))  # max 3 mesi
        dates = []
        current = self.date
        
        while current <= end:
            dates.append(current)
            current += timedelta(days=7)
        
        return dates

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'ora di inizio deve essere prima dell'ora di fine")

        # Verifica sovrapposizioni solo se l'associate è già assegnato
        if hasattr(self, 'associate') and self.associate is not None:
            overlapping = Availability.objects.filter(
                associate=self.associate,
                day_of_week=self.day_of_week,
                is_available=True
            ).exclude(pk=self.pk)

            for slot in overlapping:
                if (self.start_time < slot.end_time and self.end_time > slot.start_time):
                    raise ValidationError("Questo orario si sovrappone con un altro slot di disponibilità")