import os
import json
import tempfile
import numpy as np
from django.core.files.uploadedfile import UploadedFile

def _generate_fake_waveform(samples: int = 100) -> list:
    """
    Genera una forma d'onda simulata quando non è possibile processare il file audio
    """
    import math
    # Genera una forma d'onda sinusoidale base
    waveform = [abs(math.sin(2 * math.pi * i / 50)) * 0.8 for i in range(samples)]
    return waveform

def generate_waveform(audio_file: UploadedFile, samples: int = 100) -> list:
    """
    Genera dati waveform da un file audio
    
    Args:
        audio_file: File audio caricato
        samples: Numero di campioni per il waveform
        
    Returns:
        list: Lista di valori normalizzati per il waveform o una forma d'onda simulata se non è possibile processare il file
    """
    try:
        # Prova a importare le librerie necessarie
        from pydub import AudioSegment
        import numpy as np
        
        # Salva temporaneamente il file
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(audio_file.name)[1], delete=False) as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
        
        try:
            # Carica l'audio con pydub
            audio = AudioSegment.from_file(temp_file.name)
            
            # Converti in array numpy
            samples_array = np.array(audio.get_array_of_samples())
            
        except Exception as e:
            # Se fallisce, genera una forma d'onda simulata
            return _generate_fake_waveform(samples)
            
    except ImportError:
        # Se mancano le librerie, genera una forma d'onda simulata
        return _generate_fake_waveform(samples)
        
        # Calcola la media dei campioni
        samples_per_chunk = len(samples_array) // samples
        waveform = []
        
        for i in range(samples):
            start = i * samples_per_chunk
            end = start + samples_per_chunk
            chunk = samples_array[start:end]
            amplitude = np.abs(chunk).mean()
            waveform.append(float(amplitude))
        
        # Normalizza
        max_amplitude = max(waveform)
        waveform = [w / max_amplitude for w in waveform]
        
        return waveform
    
    finally:
        # Pulisci il file temporaneo
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def get_audio_duration(audio_file: UploadedFile) -> str:
    """
    Ottiene la durata di un file audio nel formato mm:ss
    
    Args:
        audio_file: File audio caricato
        
    Returns:
        str: Durata nel formato mm:ss
    """
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(audio_file.name)[1], delete=False) as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
    
    try:
        audio = AudioSegment.from_file(temp_file.name)
        duration_ms = len(audio)
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"
    
    finally:
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
