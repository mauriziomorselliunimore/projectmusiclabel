from django.test import TestCase
from django.contrib.auth.models import User
from reviews.forms import ReviewForm
from reviews.models import Review

class ReviewFormTest(TestCase):
    def setUp(self):
        # Crea utenti di test
        self.artist_user = User.objects.create_user(
            username='testartist',
            password='testpass123'
        )
        self.associate_user = User.objects.create_user(
            username='testassociate',
            password='testpass123'
        )

    def test_artist_to_associate_form(self):
        """Test del form per recensioni da artista a professionista"""
        form_data = {
            'review_type': 'artist_to_associate',
            'rating': 4,
            'title': 'Great Service',
            'content': 'Very professional work',
            'professionalism': 5,
            'communication': 4,
            'value': 4
        }
        
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_associate_to_artist_form(self):
        """Test del form per recensioni da professionista ad artista"""
        form_data = {
            'review_type': 'associate_to_artist',
            'rating': 4,
            'title': 'Great Artist',
            'content': 'Excellent to work with',
            'reliability': 5,
            'preparation': 4,
            'collaboration': 4
        }
        
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        """Test che il form non accetta rating invalidi"""
        form_data = {
            'review_type': 'artist_to_associate',
            'rating': 6,  # Invalid rating (> 5)
            'title': 'Test Review',
            'content': 'Test content'
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_required_fields(self):
        """Test che i campi obbligatori sono validati"""
        form_data = {
            'review_type': 'artist_to_associate',
            # Mancano i campi obbligatori
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)

    def test_review_type_specific_fields(self):
        """Test che i campi specifici per tipo di recensione sono richiesti"""
        # Test campi per recensione da artista a professionista
        form_data = {
            'review_type': 'artist_to_associate',
            'rating': 4,
            'title': 'Test',
            'content': 'Test content',
            # Mancano i campi specifici
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('professionalism', form.errors)
        self.assertIn('communication', form.errors)
        self.assertIn('value', form.errors)

        # Test campi per recensione da professionista ad artista
        form_data = {
            'review_type': 'associate_to_artist',
            'rating': 4,
            'title': 'Test',
            'content': 'Test content',
            # Mancano i campi specifici
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('reliability', form.errors)
        self.assertIn('preparation', form.errors)
        self.assertIn('collaboration', form.errors)

    def test_title_max_length(self):
        """Test che il titolo non superi la lunghezza massima"""
        form_data = {
            'review_type': 'artist_to_associate',
            'rating': 4,
            'title': 'A' * 101,  # Supera il limite di 100 caratteri
            'content': 'Test content',
            'professionalism': 5,
            'communication': 4,
            'value': 4
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_content_max_length(self):
        """Test che il contenuto non superi la lunghezza massima"""
        form_data = {
            'review_type': 'artist_to_associate',
            'rating': 4,
            'title': 'Test Review',
            'content': 'A' * 1001,  # Supera il limite di 1000 caratteri
            'professionalism': 5,
            'communication': 4,
            'value': 4
        }
        
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
