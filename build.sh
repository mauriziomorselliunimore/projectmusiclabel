#!/bin/bash

# Funzione per eseguire comandi PostgreSQL
__temp_psql() {
    psql $DATABASE_URL -v ON_ERROR_STOP=1 "$@"
}

# Funzione per gestire errori
handle_error() {
    echo "❌ Errore: $1"
    exit 1
}

echo "🚀 Avvio processo di build..."

# Installa le dipendenze Python
echo "📦 Installazione dipendenze..."
pip install -r requirements.txt || handle_error "Installazione dipendenze base fallita"
pip install -r requirements_audio.txt || handle_error "Installazione dipendenze audio fallita"

# Verifica se ffmpeg è già installato
if ! command -v ffmpeg &> /dev/null; then
    echo "🎵 ffmpeg non trovato, salto l'installazione in ambiente read-only..."
    echo "⚠️ Assicurarsi che ffmpeg sia installato nell'immagine Docker"
else
    echo "✅ ffmpeg già installato"
fi

# Reset del database
echo "🗑️ Reset del database..."
psql $DATABASE_URL -f reset_db.sql || handle_error "Reset del database fallito"

# Esegue le migrazioni del database per ogni app in ordine
echo "🔄 Creazione migrazioni per ogni app..."
for app in accounts artists associates; do
    echo "  ⚡ Creazione migrazioni per $app..."
    python manage.py makemigrations $app --noinput || handle_error "Creazione migrazioni per $app fallita"
done

echo "🔄 Applicazione migrazioni..."
python manage.py migrate --noinput || handle_error "Applicazione migrazioni fallita"

# Pulisce i file statici vecchi
echo "🧹 Pulizia file statici..."
rm -rf staticfiles/* || handle_error "Pulizia file statici fallita"

# Raccoglie i file statici
echo "📥 Raccolta file statici..."
python manage.py collectstatic --no-input || handle_error "Raccolta file statici fallita"

# Crea le migrazioni per tutte le app in ordine corretto
echo "🔄 Creazione migrazioni per tutte le app..."
for app in accounts artists associates booking core messaging api; do
    echo "  ⚡ Creazione migrazioni per $app..."
    python manage.py makemigrations $app --noinput || echo "Nota: Nessuna migrazione necessaria per $app"
done

# Applica tutte le migrazioni in ordine corretto
echo "🔄 Applicazione migrazioni..."
python manage.py migrate --noinput

# Crea un superuser se non esiste
echo "👤 Creazione superuser di default..."
python manage.py shell << 'EOPY'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✅ Superuser 'admin' creato con successo")
else:
    print("ℹ️ Superuser 'admin' già esistente")
EOPY
python manage.py migrate --noinput --run-syncdb

# Raccoglie i file statici
python manage.py collectstatic --noinput

# Invia i messaggi di benvenuto
python manage.py send_welcome_messages
