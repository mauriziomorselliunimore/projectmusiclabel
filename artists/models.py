from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from record_label.storage import AudioFileStorage

def validate_audio_file_size(value):
    filesize = value.size
    max_size = 10 * 1024 * 1024  # 10MB massimo
    if filesize > max_size:
        raise ValidationError(
            f"Il file non può superare i 10MB. Per file più grandi, "
            f"usa un servizio esterno come SoundCloud o YouTube"
        )

ARTIST_ICONS = [
    ('bi-person-circle', 'Persona'),
    ('bi-music-note', 'Nota Musicale'),
    ('bi-mic', 'Microfono'),
    ('bi-vinyl', 'Vinile'),
    ('bi-headphones', 'Cuffie'),
    ('bi-speaker', 'Speaker'),
    ('bi-soundwave', 'Onda Sonora'),
    ('bi-boombox', 'Boombox'),
    ('bi-stars', 'Stelle'),
    ('bi-lightning', 'Fulmine'),
]

MUSIC_GENRES = [
    ('rock', 'Rock'),
    ('pop', 'Pop'),
    ('hip-hop', 'Hip-Hop'),
    ('electronic', 'Electronic'),
    ('jazz', 'Jazz'),
    ('blues', 'Blues'),
    ('country', 'Country'),
    ('reggae', 'Reggae'),
    ('folk', 'Folk'),
    ('classical', 'Classical'),
    ('r&b', 'R&B'),
    ('indie', 'Indie'),
    ('punk', 'Punk'),
    ('metal', 'Metal'),
    ('funk', 'Funk'),
    ('other', 'Altro'),
]

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100, help_text="Nome d'arte")
    profile_icon = models.CharField(max_length=50, choices=ARTIST_ICONS, default='bi-person-circle', null=True, blank=True, help_text="Icona del profilo")
    profile_icon_color = models.CharField(max_length=7, default='#ff2e88', null=True, blank=True, help_text="Colore dell'icona (es. #ff2e88)")
    genres = models.CharField(max_length=200, help_text="Generi musicali separati da virgola")
    bio = models.TextField(max_length=1000, blank=True)
    
    # Social Media Links
    spotify_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Profile Info
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.stage_name or self.user.get_full_name()
    
    def get_absolute_url(self):
        return reverse('artists:detail', kwargs={'pk': self.pk})
    
    def get_genres_list(self):
        return [g.strip() for g in self.genres.split(',') if g.strip()]

class Demo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='demos')
    title = models.CharField(max_length=200)
    external_audio_url = models.URLField(blank=True, help_text="Link a SoundCloud, YouTube, Spotify, etc.")
    audio_file = models.FileField(
        upload_to='audio_files/%Y/%m/%d/',
        storage=AudioFileStorage(),
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
            validate_audio_file_size
        ],
        blank=True,
        null=True,
        help_text="File audio (max 10MB, formati: MP3, WAV)"
    )
    genre = models.CharField(max_length=50, choices=MUSIC_GENRES)
    description = models.TextField(max_length=500, blank=True)
    duration = models.CharField(max_length=10, blank=True, help_text="mm:ss")
    waveform_data = models.JSONField(null=True, blank=True, help_text="Dati per la visualizzazione della forma d'onda")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.artist.stage_name} - {self.title}"
    
    def clean(self):
        """Validazione del modello"""
        super().clean()
        if not self.external_audio_url and not self.audio_file:
            raise ValidationError("È necessario fornire un file audio o un URL esterno")
        if self.external_audio_url and self.audio_file:
            raise ValidationError("Non è possibile fornire sia un file audio che un URL esterno")

    def save(self, *args, **kwargs):
        """Override del metodo save per gestire il waveform"""
        if self.audio_file and not self.waveform_data:
            # TODO: Implementare la generazione del waveform
            pass
        super().save(*args, **kwargs)

    def get_platform(self):
        """Identifica la piattaforma dal URL"""
        if not self.external_audio_url:
            return None
        
        url = self.external_audio_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'soundcloud.com' in url:
            return 'soundcloud'
        elif 'spotify.com' in url:
            return 'spotify'
        elif 'bandcamp.com' in url:
            return 'bandcamp'
        else:
            return 'other'
            
    def get_audio_url(self):
        """Restituisce l'URL dell'audio, sia esso file locale o esterno"""
        if self.audio_file:
            return self.audio_file.url
        return self.external_audio_url