from django.test import TestCase
from django.contrib.auth.models import User
from artists.models import Artist, Demo
from django.core.exceptions import ValidationError
from django.urls import reverse

class ArtistModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crea un utente di test
        cls.test_user = User.objects.create_user(
            username='testartist',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='Artist'
        )
        
        # Crea un artista di test
        cls.test_artist = Artist.objects.create(
            user=cls.test_user,
            stage_name='Test Stage Name',
            genres='rock, pop',
            bio='Test biography',
            location='Test Location',
            profile_icon='bi-music-note',
            profile_icon_color='#ff2e88'
        )

    def test_artist_creation(self):
        """Test che l'artista viene creato correttamente"""
        self.assertEqual(self.test_artist.stage_name, 'Test Stage Name')
        self.assertEqual(self.test_artist.user.username, 'testartist')
        self.assertEqual(self.test_artist.genres, 'rock, pop')

    def test_artist_str_method(self):
        """Test del metodo __str__"""
        self.assertEqual(str(self.test_artist), 'Test Stage Name')

    def test_get_absolute_url(self):
        """Test che l'URL assoluto viene generato correttamente"""
        expected_url = reverse('artists:detail', kwargs={'pk': self.test_artist.pk})
        self.assertEqual(self.test_artist.get_absolute_url(), expected_url)

    def test_get_genres_list(self):
        """Test che il metodo get_genres_list funziona correttamente"""
        genres_list = self.test_artist.get_genres_list()
        self.assertEqual(genres_list, ['rock', 'pop'])
        self.assertEqual(len(genres_list), 2)

    def test_default_icon_values(self):
        """Test che i valori predefiniti delle icone sono corretti"""
        new_artist = Artist.objects.create(
            user=User.objects.create_user(username='another', password='pass123'),
            stage_name='Another Artist'
        )
        self.assertEqual(new_artist.profile_icon, 'bi-person-circle')
        self.assertEqual(new_artist.profile_icon_color, '#ff2e88')

    def test_icon_validation(self):
        """Test che le icone sono validate correttamente"""
        # Test con un'icona valida
        self.test_artist.profile_icon = 'bi-music-note'
        self.test_artist.full_clean()  # Non dovrebbe sollevare eccezioni

        # Test con un'icona non valida
        self.test_artist.profile_icon = 'invalid-icon'
        with self.assertRaises(ValidationError):
            self.test_artist.full_clean()

class DemoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crea un utente e un artista di test
        test_user = User.objects.create_user(username='testartist', password='testpass123')
        cls.test_artist = Artist.objects.create(
            user=test_user,
            stage_name='Test Artist'
        )
        
        # Crea una demo di test
        cls.test_demo = Demo.objects.create(
            artist=cls.test_artist,
            title='Test Demo',
            genre='rock',
            external_audio_url='https://soundcloud.com/test/demo',
            description='Test description',
            duration='3:45'
        )

    def test_demo_creation(self):
        """Test che la demo viene creata correttamente"""
        self.assertEqual(self.test_demo.title, 'Test Demo')
        self.assertEqual(self.test_demo.artist, self.test_artist)
        self.assertTrue(self.test_demo.is_public)  # Test del valore predefinito

    def test_demo_str_method(self):
        """Test del metodo __str__"""
        expected_str = f"{self.test_artist.stage_name} - Test Demo"
        self.assertEqual(str(self.test_demo), expected_str)

    def test_get_platform(self):
        """Test che il metodo get_platform identifica correttamente le piattaforme"""
        # Test SoundCloud
        self.test_demo.external_audio_url = 'https://soundcloud.com/test'
        self.assertEqual(self.test_demo.get_platform(), 'soundcloud')

        # Test YouTube
        self.test_demo.external_audio_url = 'https://youtube.com/watch?v=123'
        self.assertEqual(self.test_demo.get_platform(), 'youtube')

        # Test Spotify
        self.test_demo.external_audio_url = 'https://open.spotify.com/track/123'
        self.assertEqual(self.test_demo.get_platform(), 'spotify')

        # Test URL sconosciuto
        self.test_demo.external_audio_url = 'https://unknown.com/test'
        self.assertEqual(self.test_demo.get_platform(), 'other')

        # Test URL vuoto
        self.test_demo.external_audio_url = ''
        self.assertIsNone(self.test_demo.get_platform())
