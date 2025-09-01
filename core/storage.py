import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

def configure_cloudinary():
    """Configura Cloudinary con le credenziali dall'ambiente"""
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

def upload_file(file, resource_type="auto", folder="general"):
    """
    Carica un file su Cloudinary
    resource_type può essere "image", "video", "raw" o "auto"
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            resource_type=resource_type,
            folder=folder,
            use_filename=True,
            unique_filename=True
        )
        return result['secure_url']
    except Exception as e:
        print(f"Errore caricamento su Cloudinary: {str(e)}")
        return None

def delete_file(public_id):
    """Elimina un file da Cloudinary usando il suo public_id"""
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result['result'] == 'ok'
    except Exception as e:
        print(f"Errore eliminazione da Cloudinary: {str(e)}")
        return False

def create_audio_thumbnail(audio_url):
    """Crea una thumbnail per un file audio (forma d'onda)"""
    try:
        result = cloudinary.CloudinaryImage(audio_url).waveform(
            color="white",
            background="rgb(99,102,241)",
            width=600,
            height=120
        )
        return result.build_url()
    except Exception as e:
        print(f"Errore creazione waveform: {str(e)}")
        return None
