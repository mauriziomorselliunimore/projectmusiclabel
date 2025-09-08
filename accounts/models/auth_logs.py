from django.db import models
from django.contrib.auth.models import User

class LoginLog(models.Model):
    """Log degli accessi degli utenti"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField()
    success = models.BooleanField()
    location = models.CharField(max_length=255, blank=True, null=True)  # Per geolocalizzazione IP (opzionale)
    device_type = models.CharField(max_length=50, blank=True, null=True)  # Mobile/Desktop/Tablet

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
        ]

    def __str__(self):
        status = "successo" if self.success else "fallito"
        return f"Accesso {status} da {self.ip_address} - {self.timestamp}"
