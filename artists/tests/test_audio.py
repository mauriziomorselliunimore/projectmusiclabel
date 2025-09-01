import os
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from artists.models import Artist, Demo
from django.core.exceptions import ValidationError
from django.conf import settings

# Directory temporanea per i test dei media
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class AudioUploadTest(TestCase):
    def setUp(self):
        # Crea un utente e un artista di test
        self.test_user = User.objects.create_user(username='testartist', password='testpass123')
        self.test_artist = Artist.objects.create(
            user=self.test_user,
            stage_name='Test Artist'
        )
        
        # Crea un file audio di test
        self.audio_file = SimpleUploadedFile(
            "test_audio.mp3",
            b"file_content",
            content_type="audio/mpeg"
        )

    def tearDown(self):
        # Pulisci i file di test
        for root, dirs, files in os.walk(TEMP_MEDIA_ROOT):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(TEMP_MEDIA_ROOT)

    def test_audio_file_upload(self):
        """Test che il file audio viene caricato correttamente"""
        demo = Demo.objects.create(
            artist=self.test_artist,
            title='Test Audio Demo',
            genre='rock',
            audio_file=self.audio_file
        )
        
        self.assertTrue(os.path.exists(demo.audio_file.path))
        self.assertEqual(demo.get_platform(), None)  # Nessuna piattaforma esterna

    def test_audio_file_validation(self):
        """Test della validazione del file audio"""
        # Test file non valido
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"invalid_content",
            content_type="text/plain"
        )
        
        with self.assertRaises(ValidationError):
            demo = Demo(
                artist=self.test_artist,
                title='Invalid Demo',
                genre='rock',
                audio_file=invalid_file
            )
            demo.full_clean()

    def test_exclusive_audio_source(self):
        """Test che non si possono avere sia file che URL esterno"""
        with self.assertRaises(ValidationError):
            demo = Demo(
                artist=self.test_artist,
                title='Double Audio Demo',
                genre='rock',
                audio_file=self.audio_file,
                external_audio_url='https://soundcloud.com/test'
            )
            demo.full_clean()

    def test_waveform_generation(self):
        """Test della generazione del waveform"""
        # Crea un file audio valido per il test
        import wave
        import struct

        # Crea un file WAV di test
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            wav_file = wave.open(temp_wav.name, 'w')
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(44100)  # 44.1kHz
            
            # Genera un secondo di silenzio
            for _ in range(44100):
                value = struct.pack('h', 0)
                wav_file.writeframes(value)
            wav_file.close()

            # Leggi il file per l'upload
            with open(temp_wav.name, 'rb') as f:
                test_wav = SimpleUploadedFile(
                    "test_audio.wav",
                    f.read(),
                    content_type="audio/wav"
                )

        demo = Demo.objects.create(
            artist=self.test_artist,
            title='Waveform Test Demo',
            genre='rock',
            audio_file=test_wav
        )

        # Verifica che il waveform sia stato generato
        self.assertIsNotNone(demo.waveform_data)
        self.assertTrue(isinstance(demo.waveform_data, list))
        
        # Pulisci
        os.unlink(temp_wav.name)
