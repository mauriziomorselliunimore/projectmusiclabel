from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from reviews.models import Review

class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crea utenti di test
        cls.artist_user = User.objects.create_user(
            username='testartist',
            password='testpass123',
            email='artist@test.com'
        )
        cls.associate_user = User.objects.create_user(
            username='testassociate',
            password='testpass123',
            email='associate@test.com'
        )
        
        # Crea una recensione di test
        cls.artist_to_associate_review = Review.objects.create(
            reviewer=cls.artist_user,
            reviewed=cls.associate_user,
            review_type='artist_to_associate',
            rating=4,
            title='Great service',
            content='Very professional service',
            professionalism=5,
            communication=4,
            value=4
        )

    def test_review_creation(self):
        """Test che la recensione viene creata correttamente"""
        self.assertEqual(self.artist_to_associate_review.rating, 4)
        self.assertEqual(self.artist_to_associate_review.professionalism, 5)
        self.assertEqual(self.artist_to_associate_review.title, 'Great service')

    def test_invalid_review_type(self):
        """Test che non si possono creare recensioni con tipo invalido"""
        with self.assertRaises(ValidationError):
            review = Review(
                reviewer=self.artist_user,
                reviewed=self.associate_user,
                review_type='invalid_type',
                rating=4,
                title='Test',
                content='Test content'
            )
            review.full_clean()

    def test_rating_constraints(self):
        """Test che i rating devono essere tra 1 e 5"""
        with self.assertRaises(ValidationError):
            review = Review(
                reviewer=self.artist_user,
                reviewed=self.associate_user,
                review_type='artist_to_associate',
                rating=6,  # Invalid rating
                title='Test',
                content='Test content'
            )
            review.full_clean()

    def test_unique_reviewer_reviewed(self):
        """Test che non si possono creare recensioni duplicate"""
        with self.assertRaises(ValidationError):
            duplicate_review = Review(
                reviewer=self.artist_user,
                reviewed=self.associate_user,
                review_type='artist_to_associate',
                rating=3,
                title='Duplicate review',
                content='This should fail'
            )
            duplicate_review.full_clean()

    def test_str_method(self):
        """Test del metodo __str__"""
        expected_str = f"Recensione di {self.artist_user} per {self.associate_user}"
        self.assertEqual(str(self.artist_to_associate_review), expected_str)

    def test_review_type_specific_fields(self):
        """Test che i campi specifici per tipo di recensione sono validati correttamente"""
        # Test recensione da artista a professionista
        artist_review = Review(
            reviewer=self.artist_user,
            reviewed=self.associate_user,
            review_type='artist_to_associate',
            rating=4,
            title='Test',
            content='Test content',
            professionalism=5,
            communication=4,
            value=4
        )
        artist_review.full_clean()  # Non dovrebbe sollevare eccezioni

        # Test recensione da professionista ad artista
        associate_review = Review(
            reviewer=self.associate_user,
            reviewed=self.artist_user,
            review_type='associate_to_artist',
            rating=4,
            title='Test',
            content='Test content',
            reliability=5,
            preparation=4,
            collaboration=4
        )
        associate_review.full_clean()  # Non dovrebbe sollevare eccezioni
