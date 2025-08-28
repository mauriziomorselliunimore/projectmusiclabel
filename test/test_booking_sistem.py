# tests/test_booking_system.py
class BookingSystemTestCase(TestCase):
    def setUp(self):
        self.artist_user = User.objects.create_user('artist_test', 'test@test.com', 'pass')
        self.associate_user = User.objects.create_user('associate_test', 'test2@test.com', 'pass')
        
        Profile.objects.create(user=self.artist_user, user_type='artist')
        Profile.objects.create(user=self.associate_user, user_type='associate')
        
        self.artist = Artist.objects.create(
            user=self.artist_user, 
            stage_name='Test Artist',
            genres='Rock, Pop'
        )
        self.associate = Associate.objects.create(
            user=self.associate_user,
            specialization='Sound Engineer',
            hourly_rate=50.00
        )
    
    def test_booking_conflict_prevention(self):
        """Test prevenzione conflitti orari"""
        session_time = timezone.now() + timedelta(days=1)
        
        # Prima prenotazione
        booking1 = Booking.objects.create(
            artist=self.artist,
            associate=self.associate,
            session_date=session_time,
            duration_hours=2,
            status='confirmed'
        )
        
        # Seconda prenotazione sovrapposta dovrebbe fallire
        booking2 = Booking(
            artist=self.artist,
            associate=self.associate,
            session_date=session_time + timedelta(hours=1),
            duration_hours=2,
            status='pending'
        )
        
        with self.assertRaises(ValidationError):
            booking2.full_clean()
    
    def test_automatic_cost_calculation(self):
        """Test calcolo automatico costo"""
        booking = Booking.objects.create(
            artist=self.artist,
            associate=self.associate,
            session_date=timezone.now() + timedelta(days=1),
            duration_hours=3,
        )
        
        self.assertEqual(booking.total_cost, 150.00)  # 3 * 50€
    
    def test_booking_workflow_states(self):
        """Test workflow stati booking"""
        booking = Booking.objects.create(
            artist=self.artist,
            associate=self.associate,
            session_date=timezone.now() + timedelta(days=1),
            duration_hours=2,
        )
        
        self.assertEqual(booking.status, 'pending')
        
        booking.status = 'confirmed'
        booking.save()
        
        self.assertTrue(booking.is_upcoming)
        self.assertFalse(booking.can_be_cancelled)  # < 24h

# tests/test_models.py
class ArtistModelTest(TestCase):
    def test_get_genres_list(self):
        artist = Artist(genres='Rock, Pop, Jazz')
        expected = ['Rock', 'Pop', 'Jazz']
        self.assertEqual(artist.get_genres_list(), expected)
    
    def test_get_genres_list_with_spaces(self):
        artist = Artist(genres='Rock ,  Pop,Jazz  ')
        expected = ['Rock', 'Pop', 'Jazz']
        self.assertEqual(artist.get_genres_list(), expected)

# tests/test_views.py
class ArtistViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        Profile.objects.create(user=self.user, user_type='artist')
        
    def test_artist_creation_requires_login(self):
        response = self.client.get('/artists/create/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_artist_creation_success(self):
        self.client.login(username='test', password='pass')
        response = self.client.post('/artists/create/', {
            'stage_name': 'Test Artist',
            'genres': 'Rock, Pop',
            'bio': 'Test bio',
            'location': 'Rome',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Artist.objects.filter(stage_name='Test Artist').exists())
    
    def test_search_functionality(self):
        Artist.objects.create(
            user=self.user,
            stage_name='Rock Star',
            genres='Rock, Metal'
        )
        
        response = self.client.get('/artists/?search=Rock')
        self.assertContains(response, 'Rock Star')

# tests/test_forms.py
class FormValidationTest(TestCase):
    def test_demo_form_valid_url(self):
        form = DemoForm({
            'title': 'Test Demo',
            'external_audio_url': 'https://soundcloud.com/test/demo',
            'genre': 'rock',
            'is_public': True
        })
        self.assertTrue(form.is_valid())
    
    def test_demo_form_invalid_url(self):
        form = DemoForm({
            'title': 'Test Demo',
            'external_audio_url': 'invalid-url',
            'genre': 'rock',
        })
        self.assertFalse(form.is_valid())

# tests/test_integration.py
class BookingIntegrationTest(TestCase):
    """Test end-to-end booking workflow"""
    
    def test_complete_booking_flow(self):
        # Setup users
        artist_user = User.objects.create_user('artist', 'artist@test.com', 'pass')
        associate_user = User.objects.create_user('associate', 'associate@test.com', 'pass')
        
        # Setup profiles
        Profile.objects.create(user=artist_user, user_type='artist')
        Profile.objects.create(user=associate_user, user_type='associate')
        
        # Setup artist/associate
        artist = Artist.objects.create(user=artist_user, stage_name='Test Artist')
        associate = Associate.objects.create(
            user=associate_user, 
            specialization='Producer',
            hourly_rate=40.00
        )
        
        # Test booking creation
        self.client.login(username='artist', password='pass')
        
        session_date = (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        response = self.client.post(f'/booking/create/{associate.id}/', {
            'session_date': session_date,
            'session_time': '14:00',
            'duration_hours': 3,
            'booking_type': 'recording',
            'location': 'Test Studio',
            'notes': 'Test recording session'
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Verify booking created
        booking = Booking.objects.get(artist=artist, associate=associate)
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.total_cost, 120.00)  # 3 * 40€
        
        # Test associate confirmation
        self.client.login(username='associate', password='pass')
        response = self.client.post(f'/booking/{booking.id}/update-status/', {
            'status': 'confirmed'
        })
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')

# Comando per test coverage
# pip install coverage
# coverage run --source='.' manage.py test
# coverage report -m
# coverage html  # Genera report HTML