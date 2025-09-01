from django.db import models
from django.contrib.auth.models import User

class CollaborationProposal(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('accepted', 'Accettata'),
        ('rejected', 'Rifiutata'),
        ('counter', 'Controproposta'),
    ]
    
    TYPE_CHOICES = [
        ('production', 'Produzione Musicale'),
        ('recording', 'Sessioni Registrazione'),
        ('mixing', 'Mixing & Mastering'),
        ('live', 'Performance Live'),
        ('songwriting', 'Songwriting'),
        ('other', 'Altro'),
    ]
    
    TIMELINE_CHOICES = [
        ('asap', 'Il prima possibile'),
        ('week', 'Entro una settimana'),
        ('month', 'Entro un mese'),
        ('flexible', 'Flessibile'),
    ]
    
    MODE_CHOICES = [
        ('remote', 'Lavoro remoto'),
        ('studio', 'In studio'),
        ('hybrid', 'Misto (remoto + studio)'),
        ('flexible', 'Da definire'),
    ]
    
    # Fields
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    reference_links = models.TextField(blank=True, null=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_message = models.TextField(blank=True, null=True)
    
    # Counter proposal tracking
    counter_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    counter_notes = models.TextField(blank=True, null=True)
    
    # Message reference
    original_message = models.ForeignKey('messaging.Message', on_delete=models.SET_NULL, null=True, related_name='proposals')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Proposta da {self.sender} a {self.receiver} ({self.get_status_display()})"
    
    def get_reference_links(self):
        """Returns a list of reference links"""
        if not self.reference_links:
            return []
        return [link.strip() for link in self.reference_links.split('\n') if link.strip()]
