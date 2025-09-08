from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .constants import MUSIC_GENRES

def validate_audio_file_size(value):
    """Validate that the audio file size is not larger than 10MB"""
    filesize = value.size
    max_size = 10 * 1024 * 1024  # 10MB massimo
    if filesize > max_size:
        raise ValidationError(
            f"Il file non può superare i 10MB. Per file più grandi, "
            f"usa un servizio esterno come SoundCloud o YouTube"
        )

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
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Media files
    profile_image = models.ImageField(upload_to='artist_images/', blank=True)
    background_image = models.ImageField(upload_to='artist_backgrounds/', blank=True)
    press_kit = models.FileField(upload_to='press_kits/', blank=True)
    
    class Meta:
        ordering = ['stage_name']
        verbose_name = 'Artista'
        verbose_name_plural = 'Artisti'

    def __str__(self):
        return self.stage_name

    def get_social_links(self):
        """Returns a dictionary of social media links"""
        return {
            'spotify': self.spotify_url,
            'youtube': self.youtube_url,
            'soundcloud': self.soundcloud_url,
            'instagram': self.instagram_url,
            'facebook': self.facebook_url,
            'twitter': self.twitter_url
        }

    def get_genres_list(self):
        """Returns a list of genres"""
        return [g.strip() for g in self.genres.split(',')] if self.genres else []

    def has_complete_profile(self):
        """Checks if the artist has completed their profile"""
        return all([
            self.stage_name,
            self.bio,
            self.genres,
            self.location,
            self.profile_image
        ])
