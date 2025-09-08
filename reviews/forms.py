from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'rating', 'title', 'content',
            'professionalism', 'communication', 'value',
            'reliability', 'preparation', 'collaboration'
        ]
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titolo della recensione'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Scrivi la tua recensione...'
            }),
            'professionalism': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            }),
            'communication': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            }),
            'reliability': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            }),
            'preparation': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            }),
            'collaboration': forms.NumberInput(attrs={
                'class': 'form-control rating-input',
                'min': '1',
                'max': '5'
            })
        }

    def __init__(self, *args, review_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        if review_type == 'artist_to_associate':
            # Rimuovi i campi non pertinenti per recensioni ad associati
            del self.fields['reliability']
            del self.fields['preparation']
            del self.fields['collaboration']
        elif review_type == 'associate_to_artist':
            # Rimuovi i campi non pertinenti per recensioni ad artisti
            del self.fields['professionalism']
            del self.fields['communication']
            del self.fields['value']
"""
All review forms have been removed as reviews are no longer needed.
"""
