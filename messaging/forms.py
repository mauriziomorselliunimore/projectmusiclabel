from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """Form per inviare messaggi"""
    
    class Meta:
        model = Message
        fields = ['message']  # CORRETTO: 'message' non 'content'
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Scrivi il tuo messaggio...',
                'required': True
            })
        }
        labels = {
            'message': 'Messaggio'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({
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


class CompleteMessageForm(forms.ModelForm):
    """Form completo per messaggi con soggetto e tipo"""
    
    class Meta:
        model = Message
        fields = ['message_type', 'subject', 'message']
        widgets = {
            'message_type': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Oggetto del messaggio...'
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Scrivi il tuo messaggio...',
                    'style': 'resize: none; border-radius: 0.75rem;'
                }
            )
        }
        labels = {
            'message_type': 'Tipo di messaggio',
            'subject': 'Oggetto',
            'message': 'Messaggio'
        }
            'message_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Oggetto del messaggio...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Scrivi il tuo messaggio...'
            })
        }
        labels = {
            'message_type': 'Tipo Messaggio',
            'subject': 'Oggetto',
            'message': 'Messaggio'
        }