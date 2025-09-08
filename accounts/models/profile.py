from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    PROFILE_ICONS = [
        ('bi-person', 'Persona'),
        ('bi-person-badge', 'Badge'),
        ('bi-person-circle', 'Cerchio'),
        ('bi-emoji-smile', 'Sorriso'),
        ('bi-star', 'Stella'),
        ('bi-heart', 'Cuore'),
        ('bi-gem', 'Gemma'),
        ('bi-award', 'Premio'),
        ('bi-lightning', 'Fulmine'),
        ('bi-shield', 'Scudo'),
    ]

    USER_TYPES = [
        ('artist', 'Artista'),
        ('associate', 'Associato'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_icon = models.CharField(max_length=50, choices=PROFILE_ICONS, default='bi-person-circle', null=True, blank=True, help_text="Icona del profilo")
    profile_icon_color = models.CharField(max_length=7, default='#6366f1', null=True, blank=True, help_text="Colore dell'icona (es. #6366f1)")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # URL esterno invece di file upload
    external_avatar_url = models.URLField(
        blank=True, 
        help_text="Link a foto profilo esterna (Imgur, Google Drive, Gravatar, etc.)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    def get_avatar_url(self):
        """Ritorna l'URL dell'avatar dell'utente"""
        if self.external_avatar_url:
            return self.external_avatar_url
        return f"https://ui-avatars.com/api/?name={self.user.get_full_name()}&background=6366f1&color=fff"
    
    def get_absolute_url(self):
        if self.user_type == 'artist':
            try:
                return reverse('artists:detail', kwargs={'pk': self.user.artist.pk})
            except:
                return reverse('artists:create')
        else:
            try:
                return reverse('associates:detail', kwargs={'pk': self.user.associate.pk})
            except:
                return reverse('associates:create')
