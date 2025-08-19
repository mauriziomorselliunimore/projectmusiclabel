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
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    def get_absolute_url(self):
        if self.user_type == 'artist':
            return reverse('artists:detail', kwargs={'pk': self.user.pk})
        else:
            return reverse('associates:detail', kwargs={'pk': self.user.pk})