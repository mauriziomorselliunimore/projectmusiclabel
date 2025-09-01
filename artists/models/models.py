from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .constants import MUSIC_GENRES

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    genres = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Social media
    spotify_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    # Profile customization
    profile_icon = models.CharField(max_length=50, default="bi-music-note-beamed")
    profile_icon_color = models.CharField(max_length=50, default="#ffffff")

    def __str__(self):
        return self.stage_name

    def get_genres_list(self):
        """Return genres as a list"""
        if not self.genres:
            return []
        return [genre.strip() for genre in self.genres.split(',')]

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

    def __str__(self):
        return f"{self.artist.stage_name} - {self.title}"
