from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from artists.models import Artist
from associates.models import Associate
from booking.models import QuoteRequest

class QuoteRequestViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.artist_user = User.objects.create_user(username='artist3', password='testpass')
        self.associate_user = User.objects.create_user(username='associate3', password='testpass')
        self.artist = Artist.objects.create(user=self.artist_user, stage_name='Artista3')
        self.associate = Associate.objects.create(user=self.associate_user)
        self.client.login(username='artist3', password='testpass')

    def test_request_quote_view_get(self):
        url = reverse('request_quote', args=[self.associate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Richiesta Preventivo')

    def test_request_quote_view_post(self):
        url = reverse('request_quote', args=[self.associate.id])
        data = {'message': 'Preventivo per evento'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuoteRequest.objects.filter(artist=self.artist, associate=self.associate).exists())

    def test_view_quote_permission(self):
        quote = QuoteRequest.objects.create(artist=self.artist, associate=self.associate, message='Test')
        url = reverse('view_quote', args=[quote.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dettaglio Preventivo')
