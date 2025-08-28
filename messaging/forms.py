# messaging/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_type', 'subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Oggetto del messaggio'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Scrivi il tuo messaggio...'
            }),
            'message_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'message_type': 'Tipo Messaggio',
            'subject': 'Oggetto',
            'message': 'Messaggio',
        }
