import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurazioni per i file media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configurazioni per i file audio
AUDIO_FILE_UPLOAD_MAX_SIZE = 10 * 1024 * 1024  # 10MB
AUDIO_FILE_ALLOWED_EXTENSIONS = ['mp3', 'wav']

# Configurazioni per la validazione dei file
DEMO_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
DEMO_FILE_ALLOWED_EXTENSIONS = ['mp3', 'wav']

# Configurazioni per l'upload delle immagini del profilo
PROFILE_IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5MB
PROFILE_IMAGE_ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
