from django import forms
from .models import Artist, Demo

from accounts.models import Profile

class ArtistForm(forms.ModelForm):
    # Aggiungiamo i campi del profilo
    external_avatar_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://imgur.com/your-image.jpg',
            'class': 'form-control'
        }),
        label='URL Immagine Profilo',
        help_text='Link a una tua foto (Imgur, Google Drive, etc.)'
    )
    profile_icon = forms.ChoiceField(
        choices=Profile.PROFILE_ICONS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Icona Profilo'
    )
    profile_icon_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'form-control form-control-color'
        }),
        label='Colore Icona'
    )

    class Meta:
        model = Artist
        fields = [
            'stage_name', 'genres', 'bio', 'location', 'phone',
            'spotify_url', 'youtube_url', 'soundcloud_url', 'instagram_url'
        ]
        widgets = {
            'stage_name': forms.TextInput(attrs={'placeholder': 'Il tuo nome d\'arte'}),
            'genres': forms.TextInput(attrs={'placeholder': 'Rock, Pop, Blues (separati da virgola)'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Racconta la tua storia musicale...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Roma, Italia'}),
            'phone': forms.TextInput(attrs={'placeholder': '+39 123 456 7890'}),
            'spotify_url': forms.URLInput(attrs={'placeholder': 'https://open.spotify.com/artist/...'}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/c/...'}),
            'soundcloud_url': forms.URLInput(attrs={'placeholder': 'https://soundcloud.com/...'}),
            'instagram_url': forms.URLInput(attrs={'placeholder': 'https://instagram.com/...'}),
        }
        labels = {
            'stage_name': 'Nome d\'arte',
            'genres': 'Generi musicali',
            'bio': 'Biografia',
            'location': 'Località',
            'phone': 'Telefono',
            'spotify_url': 'Spotify',
            'youtube_url': 'YouTube',
            'soundcloud_url': 'SoundCloud',
            'instagram_url': 'Instagram',
        }

class DemoForm(forms.ModelForm):
    class Meta:
        model = Demo
        fields = ['title', 'audio_file', 'external_audio_url', 'genre', 'description', 'duration', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titolo della canzone'}),
            'audio_file': forms.FileInput(attrs={'accept': 'audio/mp3,audio/wav'}),
            'external_audio_url': forms.URLInput(attrs={'placeholder': 'https://soundcloud.com/artista/canzone'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrizione, storia dietro la canzone...'}),
            'duration': forms.TextInput(attrs={'placeholder': '3:45'}),
        }
        labels = {
            'title': 'Titolo',
            'audio_file': 'File Audio',
            'external_audio_url': 'Link Audio',
            'genre': 'Genere',
            'description': 'Descrizione',
            'duration': 'Durata',
            'is_public': 'Pubblica (visibile a tutti)',
        }

    def clean(self):
        cleaned_data = super().clean()
        audio_file = cleaned_data.get('audio_file')
        external_url = cleaned_data.get('external_audio_url')
        
        if not audio_file and not external_url:
            raise forms.ValidationError(
                "È necessario fornire un file audio o un URL esterno"
            )
        
        if audio_file and external_url:
            raise forms.ValidationError(
                "Non è possibile fornire sia un file audio che un URL esterno"
            )
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['external_audio_url'].help_text = (
            'Link a SoundCloud, YouTube, Spotify, Bandcamp, etc. '
            'Esempio: https://soundcloud.com/artista/canzone'
        )