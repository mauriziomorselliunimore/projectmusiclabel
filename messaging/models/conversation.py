from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


class Conversation(models.Model):
    """Rappresenta una conversazione tra due utenti"""
    participant_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_participant_1')
    participant_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_participant_2')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey('messaging.Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    last_message_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = [['participant_1', 'participant_2']]
    
    def __str__(self):
        return f"Conversazione: {self.participant_1.get_full_name()} - {self.participant_2.get_full_name()}"
    
    def get_other_participant(self, user):
        """Ottiene l'altro partecipante della conversazione"""
        if user == self.participant_1:
            return self.participant_2
        elif user == self.participant_2:
            return self.participant_1
        return None
    
    def update_last_message(self, message):
        """Aggiorna l'ultimo messaggio della conversazione"""
        self.last_message = message
        self.last_message_date = message.created_at
        self.updated_at = timezone.now()
        self.save(update_fields=['last_message', 'last_message_date', 'updated_at'])
    
    def has_unread_messages(self, user):
        """Controlla se ci sono messaggi non letti per l'utente"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).exists()
    
    def unread_count_for_user(self, user):
        """Conta i messaggi non letti per l'utente specificato"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=user).count()
    
    def get_absolute_url(self):
        return reverse('messaging:conversation', kwargs={'conversation_id': self.pk})
    
    @classmethod
    def get_or_create_conversation(cls, user1, user2):
        """Ottiene o crea una conversazione tra due utenti"""
        # Assicurati che user1 abbia sempre ID minore per consistenza
        if user1.id > user2.id:
            user1, user2 = user2, user1
        
        conversation = cls.objects.filter(
            Q(participant_1=user1, participant_2=user2) |
            Q(participant_1=user2, participant_2=user1)
        ).first()
        
        if not conversation:
            conversation = cls.objects.create(
                participant_1=user1,
                participant_2=user2
            )
        
        return conversation
