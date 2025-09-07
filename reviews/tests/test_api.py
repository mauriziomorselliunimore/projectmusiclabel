from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from reviews.models import Review
from api.serializers import ReviewSerializer

class ReviewAPITest(TestCase):
    def setUp(self):
        # Crea il client API
        self.client = APIClient()
        
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

    def test_get_all_reviews(self):
        """Test dell'endpoint GET per lista recensioni"""
        url = reverse('api:review-list')
        response = self.client.get(url)
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_review(self):
        """Test dell'endpoint GET per singola recensione"""
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        review = Review.objects.get(pk=self.review.pk)
        serializer = ReviewSerializer(review)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_review(self):
        """Test dell'endpoint POST per creare una recensione"""
        self.client.force_authenticate(user=self.associate_user)
        url = reverse('api:review-list')
        data = {
            'reviewed': self.artist_user.id,
            'review_type': 'associate_to_artist',
            'rating': 5,
            'title': 'New Review',
            'content': 'Great artist to work with',
            'reliability': 5,
            'preparation': 4,
            'collaboration': 5
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.latest('id').title, 'New Review')

    def test_update_review(self):
        """Test dell'endpoint PUT per aggiornare una recensione"""
        self.client.force_authenticate(user=self.artist_user)
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        data = {
            'reviewed': self.associate_user.id,
            'review_type': 'artist_to_associate',
            'rating': 5,
            'title': 'Updated Review',
            'content': 'Updated content',
            'professionalism': 5,
            'communication': 5,
            'value': 5
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Review')

    def test_delete_review(self):
        """Test dell'endpoint DELETE per eliminare una recensione"""
        self.client.force_authenticate(user=self.artist_user)
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test che gli utenti non autenticati non possono modificare recensioni"""
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        data = {'title': 'Unauthorized Update'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_user_update(self):
        """Test che gli utenti non possono modificare recensioni altrui"""
        self.client.force_authenticate(user=self.associate_user)
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        data = {
            'reviewed': self.associate_user.id,
            'review_type': 'artist_to_associate',
            'rating': 1,
            'title': 'Wrong User Update',
            'content': 'This should fail'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_review_data(self):
        """Test che i dati invalidi vengono gestiti correttamente"""
        self.client.force_authenticate(user=self.artist_user)
        url = reverse('api:review-list')
        data = {
            'reviewed': self.associate_user.id,
            'review_type': 'artist_to_associate',
            'rating': 10,  # Invalid rating
            'title': '',  # Empty title
            'content': 'Test content'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
