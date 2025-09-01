from django import forms
from django.test import TestCase
from django.contrib.auth.models import User
from artists.forms import ArtistForm, DemoForm
from artists.models import Artist

class ArtistFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crea un utente di test
        cls.test_user = User.objects.create_user(
            username='testartist',
            password='testpass123'
        )

    def test_artist_form_valid_data(self):
        """Test che il form accetta dati validi"""
        form_data = {
            'stage_name': 'Test Artist',
            'genres': 'rock, pop',
            'bio': 'Test biography',
            'location': 'Test Location',
            'phone': '+1234567890',
            'spotify_url': 'https://spotify.com/artist/test',
            'youtube_url': 'https://youtube.com/test',
            'profile_icon': 'bi-music-note',
            'profile_icon_color': '#ff2e88'
        }
        form = ArtistForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artist_form_invalid_data(self):
        """Test che il form rifiuta dati non validi"""
        form_data = {
            'stage_name': '',  # Campo richiesto
            'genres': 'rock, pop'
        }
        form = ArtistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stage_name', form.errors)

    def test_artist_form_icon_validation(self):
        """Test della validazione delle icone"""
        form_data = {
            'stage_name': 'Test Artist',
            'genres': 'rock',
            'profile_icon': 'invalid-icon',  # Icona non valida
            'profile_icon_color': '#ff2e88'
        }
        form = ArtistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('profile_icon', form.errors)

    def test_artist_form_color_validation(self):
        """Test della validazione del colore"""
        form_data = {
            'stage_name': 'Test Artist',
            'genres': 'rock',
            'profile_icon': 'bi-music-note',
            'profile_icon_color': 'not-a-color'  # Colore non valido
        }
        form = ArtistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('profile_icon_color', form.errors)

class DemoFormTest(TestCase):
    def test_demo_form_valid_data(self):
        """Test che il form della demo accetta dati validi"""
        form_data = {
            'title': 'Test Demo',
            'external_audio_url': 'https://soundcloud.com/test/demo',
            'genre': 'rock',
            'description': 'Test description',
            'duration': '3:45',
            'is_public': True
        }
        form = DemoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_demo_form_invalid_url(self):
        """Test che il form valida correttamente gli URL"""
        form_data = {
            'title': 'Test Demo',
            'external_audio_url': 'not-a-url',  # URL non valido
            'genre': 'rock'
        }
        form = DemoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('external_audio_url', form.errors)
