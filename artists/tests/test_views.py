from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from artists.models import Artist, Demo

class ArtistViewsTest(TestCase):
    def setUp(self):
        # Crea un client di test
        self.client = Client()
        
        # Crea un utente di test
        self.test_user = User.objects.create_user(
            username='testartist',
            password='testpass123',
            email='test@example.com'
        )
        
        # Crea un artista di test
        self.test_artist = Artist.objects.create(
            user=self.test_user,
            stage_name='Test Artist',
            genres='rock, pop',
            bio='Test biography',
            profile_icon='bi-music-note',
            profile_icon_color='#ff2e88'
        )

    def test_artist_list_view(self):
        """Test della vista lista artisti"""
        response = self.client.get(reverse('artists:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artists/artist_list.html')
        self.assertContains(response, 'Test Artist')
        self.assertContains(response, 'bi-music-note')

    def test_artist_detail_view(self):
        """Test della vista dettaglio artista"""
        response = self.client.get(reverse('artists:detail', args=[self.test_artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artists/artist_detail.html')
        self.assertContains(response, 'Test Artist')
        self.assertContains(response, 'Test biography')

    def test_artist_create_view_unauthenticated(self):
        """Test che gli utenti non autenticati non possono creare artisti"""
        response = self.client.get(reverse('artists:create'))
        self.assertEqual(response.status_code, 302)  # Redirect al login

    def test_artist_create_view_authenticated(self):
        """Test che gli utenti autenticati possono accedere al form di creazione"""
        self.client.login(username='testartist', password='testpass123')
        response = self.client.get(reverse('artists:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artists/artist_form.html')

    def test_artist_update_view(self):
        """Test dell'aggiornamento del profilo artista"""
        # Login come artista
        self.client.login(username='testartist', password='testpass123')
        
        # Test aggiornamento
        update_data = {
            'stage_name': 'Updated Name',
            'genres': 'jazz, blues',
            'bio': 'Updated bio',
            'profile_icon': 'bi-vinyl',
            'profile_icon_color': '#123456'
        }
        response = self.client.post(
            reverse('artists:update', args=[self.test_artist.id]),
            update_data
        )
        
        # Ricarica l'artista dal database
        self.test_artist.refresh_from_db()
        
        # Verifica che i dati siano stati aggiornati
        self.assertEqual(self.test_artist.stage_name, 'Updated Name')
        self.assertEqual(self.test_artist.genres, 'jazz, blues')
        self.assertEqual(self.test_artist.profile_icon, 'bi-vinyl')

    def test_artist_search(self):
        """Test della funzionalità di ricerca artisti"""
        # Crea alcuni artisti per il test
        User.objects.create_user(username='rock_artist', password='pass123')
        Artist.objects.create(
            user=User.objects.get(username='rock_artist'),
            stage_name='Rock Star',
            genres='rock'
        )
        
        # Test ricerca per nome
        response = self.client.get(reverse('artists:list') + '?search=Rock')
        self.assertContains(response, 'Rock Star')
        self.assertNotContains(response, 'Test Artist')
        
        # Test ricerca per genere
        response = self.client.get(reverse('artists:list') + '?genre=pop')
        self.assertContains(response, 'Test Artist')
        self.assertNotContains(response, 'Rock Star')
