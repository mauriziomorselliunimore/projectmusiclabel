from django.test import TestCase
from django.contrib.auth import get_user_model
from booking.models import QuoteRequest
from django.urls import reverse

class QuoteRequestTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.artist = User.objects.create_user(username='artist1', password='testpass')
        self.associate = User.objects.create_user(username='associate1', password='testpass')
        self.client.login(username='artist1', password='testpass')

    def test_create_quote_request(self):
        url = reverse('request_quote', args=[self.associate.id])
        data = {'description': 'Vorrei un preventivo per un evento.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(QuoteRequest.objects.filter(artist=self.artist, associate=self.associate).exists())

    def test_view_quote(self):
        quote = QuoteRequest.objects.create(artist=self.artist, associate=self.associate, description='Test', status='pending')
        url = reverse('view_quote', args=[quote.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
