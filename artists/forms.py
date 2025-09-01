from django import forms
from .models import Artist, Demo, MUSIC_GENRES, ARTIST_ICONS

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'stage_name', 'profile_icon', 'profile_icon_color', 'genres', 'bio', 'location', 'phone',
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
            'profile_icon': 'Icona del profilo',
            'profile_icon_color': 'Colore dell\'icona',
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
        fields = ['title', 'external_audio_url', 'genre', 'description', 'duration', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titolo della canzone'}),
            'external_audio_url': forms.URLInput(attrs={'placeholder': 'https://soundcloud.com/artista/canzone'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrizione, storia dietro la canzone...'}),
            'duration': forms.TextInput(attrs={'placeholder': '3:45'}),
        }
        labels = {
            'title': 'Titolo',
            'external_audio_url': 'Link Audio',
            'genre': 'Genere',
            'description': 'Descrizione',
            'duration': 'Durata',
            'is_public': 'Pubblica (visibile a tutti)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['external_audio_url'].help_text = (
            'Link a SoundCloud, YouTube, Spotify, Bandcamp, etc. '
            'Esempio: https://soundcloud.com/artista/canzone'
        )