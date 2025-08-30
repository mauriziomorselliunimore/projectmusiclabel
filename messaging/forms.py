from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """Form per inviare messaggi"""
    
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Scrivi il tuo messaggio...',
                'required': True
            })
        }
        labels = {
            'content': 'Messaggio'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'style': 'resize: none; border-radius: 0.75rem;'
        })


class QuickMessageForm(forms.Form):
    """Form rapido per messaggi in modals o sidebar"""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Messaggio rapido...',
            'style': 'resize: none; border-radius: 0.5rem;'
        }),
        max_length=500,
        label='Messaggio'
    )