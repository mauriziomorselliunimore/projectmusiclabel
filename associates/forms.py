from django import forms
from .models import Associate, PortfolioItem, Availability, SKILLS, EXPERIENCE_LEVELS

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
        fields = ['title', 'description', 'external_image_url', 'external_audio_url', 'external_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nome del progetto/lavoro'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrizione del lavoro svolto...'}),
            'external_image_url': forms.URLInput(attrs={'placeholder': 'https://imgur.com/abc123.jpg (opzionale)'}),
            'external_audio_url': forms.URLInput(attrs={'placeholder': 'https://soundcloud.com/... (opzionale)'}),
            'external_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/watch?v=... (link principale)'}),
        }
        labels = {
            'title': 'Titolo',
            'description': 'Descrizione',
            'external_image_url': 'Link Immagine',
            'external_audio_url': 'Link Audio',
            'external_url': 'Link Principale',
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available', 'note']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'note': forms.TextInput(attrs={'placeholder': 'Note opzionali sulla disponibilità'}),
        }
        labels = {
            'day_of_week': 'Giorno',
            'start_time': 'Ora inizio',
            'end_time': 'Ora fine',
            'is_available': 'Disponibile',
            'note': 'Note',
        }