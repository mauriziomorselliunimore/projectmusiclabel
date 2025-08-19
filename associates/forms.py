from django import forms
from .models import Associate, PortfolioItem, SKILLS, EXPERIENCE_LEVELS

class AssociateForm(forms.ModelForm):
    class Meta:
        model = Associate
        fields = [
            'specialization', 'skills', 'experience_level', 'hourly_rate', 
            'availability', 'bio', 'location', 'phone', 'website',
            'portfolio_description', 'years_experience', 'is_available'
        ]
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': 'Sound Engineer, Producer, Guitarist...'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Mixing, Mastering, Pro Tools, Logic Pro (separati da virgola)'}),
            'hourly_rate': forms.NumberInput(attrs={'placeholder': '25.00', 'step': '0.01'}),
            'availability': forms.TextInput(attrs={'placeholder': 'Lunedì-Venerdì 9-18, Weekend su richiesta'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'La tua esperienza professionale...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Roma, Italia'}),
            'phone': forms.TextInput(attrs={'placeholder': '+39 123 456 7890'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://tuosito.com'}),
            'portfolio_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrivi i tuoi lavori migliori...'}),
            'years_experience': forms.NumberInput(attrs={'placeholder': '5'}),
        }
        labels = {
            'specialization': 'Specializzazione principale',
            'skills': 'Competenze',
            'experience_level': 'Livello di esperienza',
            'hourly_rate': 'Tariffa oraria (€)',
            'availability': 'Disponibilità',
            'bio': 'Biografia professionale',
            'location': 'Località',
            'phone': 'Telefono',
            'website': 'Sito web',
            'portfolio_description': 'Descrizione portfolio',
            'years_experience': 'Anni di esperienza',
            'is_available': 'Disponibile per nuovi lavori',
        }

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'image', 'audio_file', 'external_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nome del progetto/lavoro'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrizione del lavoro svolto...'}),
            'external_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/watch?v=... (opzionale)'}),
        }
        labels = {
            'title': 'Titolo',
            'description': 'Descrizione',
            'image': 'Immagine',
            'audio_file': 'File Audio',
            'external_url': 'Link esterno',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'JPG, PNG (max 5MB)'
        self.fields['audio_file'].help_text = 'MP3, WAV (max 10MB)'