from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .artist import Artist
from .constants import MUSIC_GENRES

class Demo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='demos')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    audio_file = models.FileField(
        upload_to='demos/',
        validators=[FileExtensionValidator(['mp3', 'wav', 'ogg', 'm4a'])],
        blank=True,
        null=True
    )
    external_audio_url = models.URLField(blank=True, null=True)
    genre = models.CharField(max_length=50, choices=MUSIC_GENRES)
    duration = models.DurationField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Demo'
        verbose_name_plural = 'Demo'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.artist.stage_name} - {self.title}"

    def clean(self):
        """Validate that at least one audio source is provided"""
        if not self.audio_file and not self.external_audio_url:
            raise ValidationError(
                "È necessario fornire un file audio o un URL esterno"
            )

    def get_audio_source(self):
        """Returns the audio source (file or external URL)"""
        return self.audio_file.url if self.audio_file else self.external_audio_url
