from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    genre = models.CharField(max_length=50, choices=MUSIC_GENRES)
    description = models.TextField(max_length=500, blank=True)
    duration = models.CharField(max_length=10, blank=True, help_text="mm:ss")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.artist.stage_name} - {self.title}"
    
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