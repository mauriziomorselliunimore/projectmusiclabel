from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    USER_TYPES = [
        ('artist', 'Artista'),
        ('associate', 'Associato'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
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
    
    def get_avatar_url(self):
        """Restituisce l'URL dell'avatar o un placeholder"""
        if self.external_avatar_url:
            return self.external_avatar_url
        
        # Fallback: Gravatar basato sull'email
        import hashlib
        email_hash = hashlib.md5(self.user.email.lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=150"