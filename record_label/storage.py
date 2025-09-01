from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class AudioFileStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location=os.path.join(settings.MEDIA_ROOT, 'audio_files'))

    def get_valid_name(self, name):
        name = super().get_valid_name(name)
        # Aggiungi un timestamp al nome del file per evitare conflitti
        name, ext = os.path.splitext(name)
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{name}_{timestamp}{ext}"
