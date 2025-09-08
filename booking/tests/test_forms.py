from django.test import TestCase
from booking.forms import QuoteRequestForm

class QuoteRequestFormTests(TestCase):
    def test_form_valid(self):
        form = QuoteRequestForm(data={'message': 'Preventivo per evento live'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = QuoteRequestForm(data={'message': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
