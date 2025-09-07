from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Review
from artists.models import Artist
from associates.models import Associate

class ReviewViewsTest(TestCase):
    def setUp(self):
        # Crea il client di test
        self.client = Client()
        
        # Crea utenti di test
        self.artist_user = User.objects.create_user(
            username='testartist',
            password='testpass123',
            email='artist@test.com'
        )
        self.associate_user = User.objects.create_user(
            username='testassociate',
            password='testpass123',
            email='associate@test.com'
        )
        
        # Crea profili
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist'
        )
        self.associate = Associate.objects.create(
            user=self.associate_user,
            business_name='Test Associate'
        )
        
        # Crea una recensione di test
        self.review = Review.objects.create(
            reviewer=self.artist_user,
            reviewed=self.associate_user,
            review_type='artist_to_associate',
            rating=4,
            title='Test Review',
            content='Test content',
            professionalism=5,
            communication=4,
            value=4
        )

    def test_review_list_view(self):
        """Test della vista lista recensioni"""
        # Login come artista
        self.client.login(username='testartist', password='testpass123')
        
        # Test vista lista recensioni
        response = self.client.get(reverse('reviews:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_list.html')
        self.assertContains(response, 'Test Review')

    def test_review_detail_view(self):
        """Test della vista dettaglio recensione"""
        # Login come artista
        self.client.login(username='testartist', password='testpass123')
        
        # Test vista dettaglio
        response = self.client.get(reverse('reviews:detail', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_detail.html')
        self.assertContains(response, 'Test Review')
        self.assertContains(response, 'Test content')

    def test_create_review_view(self):
        """Test della creazione recensione"""
        # Login come associate
        self.client.login(username='testassociate', password='testpass123')
        
        # Dati per la nuova recensione
        review_data = {
            'review_type': 'associate_to_artist',
            'rating': 5,
            'title': 'Great Artist',
            'content': 'Excellent to work with',
            'reliability': 5,
            'preparation': 4,
            'collaboration': 5
        }
        
        # Test creazione recensione
        response = self.client.post(
            reverse('reviews:create', kwargs={'user_id': self.artist_user.id}),
            review_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect dopo il successo
        
        # Verifica che la recensione sia stata creata
        self.assertTrue(
            Review.objects.filter(
                reviewer=self.associate_user,
                reviewed=self.artist_user,
                title='Great Artist'
            ).exists()
        )

    def test_update_review_view(self):
        """Test dell'aggiornamento recensione"""
        # Login come artista
        self.client.login(username='testartist', password='testpass123')
        
        # Dati per l'aggiornamento
        update_data = {
            'review_type': 'artist_to_associate',
            'rating': 5,
            'title': 'Updated Review',
            'content': 'Updated content',
            'professionalism': 5,
            'communication': 5,
            'value': 5
        }
        
        # Test aggiornamento recensione
        response = self.client.post(
            reverse('reviews:update', kwargs={'pk': self.review.pk}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        
        # Verifica che la recensione sia stata aggiornata
        updated_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.title, 'Updated Review')
        self.assertEqual(updated_review.rating, 5)

    def test_delete_review_view(self):
        """Test dell'eliminazione recensione"""
        # Login come artista
        self.client.login(username='testartist', password='testpass123')
        
        # Test eliminazione recensione
        response = self.client.post(reverse('reviews:delete', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 302)
        
        # Verifica che la recensione sia stata eliminata
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_unauthorized_access(self):
        """Test che gli utenti non autorizzati non possono modificare recensioni altrui"""
        # Login come associate
        self.client.login(username='testassociate', password='testpass123')
        
        # Prova a modificare una recensione non propria
        update_data = {
            'title': 'Unauthorized Update',
            'content': 'This should fail'
        }
        
        response = self.client.post(
            reverse('reviews:update', kwargs={'pk': self.review.pk}),
            update_data
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
