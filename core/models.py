from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Follow(models.Model):
    """
    Modello generico per seguire artisti o associati
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
    # Campo generico per permettere di seguire sia artisti che associati
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    followed_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('follower', 'content_type', 'object_id')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.get_full_name()} segue {self.followed_object}"