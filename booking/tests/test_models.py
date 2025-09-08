from django.test import TestCase
from booking.models import QuoteRequest
from artists.models import Artist
from associates.models import Associate
from django.contrib.auth import get_user_model

class QuoteRequestModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.artist_user = User.objects.create_user(username='artist2', password='testpass')
        self.associate_user = User.objects.create_user(username='associate2', password='testpass')
        self.artist = Artist.objects.create(user=self.artist_user, stage_name='Artista2')
        self.associate = Associate.objects.create(user=self.associate_user)

    def test_create_quote_request(self):
        quote = QuoteRequest.objects.create(artist=self.artist, associate=self.associate, message='Preventivo test')
        self.assertEqual(str(quote), f"Preventivo da {self.artist.stage_name} a {self.associate.user.get_full_name()} (In attesa)")
        self.assertEqual(quote.status, 'pending')
        self.assertEqual(quote.response, '')
