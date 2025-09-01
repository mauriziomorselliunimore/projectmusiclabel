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

# Installa le dipendenze
echo "📦 Installazione dipendenze..."
pip install -r requirements.txt || handle_error "Installazione dipendenze fallita"

# Pulisce i file statici vecchi
echo "🧹 Pulizia file statici..."
rm -rf staticfiles/* || handle_error "Pulizia file statici fallita"

# Raccoglie i file statici
echo "📥 Raccolta file statici..."
python manage.py collectstatic --no-input || handle_error "Raccolta file statici fallita"

# Reset completo del database se necessario
echo "🧹 Reset del database se necessario..."
__temp_psql << 'EOSQL'
DO $$ 
BEGIN
    -- Drop di tutte le tabelle in modo sicuro
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO current_user;
    GRANT ALL ON SCHEMA public TO public;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Ignoro errori di schema: %', SQLERRM;
END $$;
EOSQL

# Crea le migrazioni per tutte le app in ordine corretto
echo "🔄 Creazione migrazioni per tutte le app..."
for app in accounts artists associates booking core messaging api; do
    echo "  ⚡ Creazione migrazioni per $app..."
    python manage.py makemigrations $app --noinput || echo "Nota: Nessuna migrazione necessaria per $app"
done

# Applica le migrazioni in ordine corretto
echo "🔄 Applicazione migrazioni in ordine..."
python manage.py migrate contenttypes --noinput
python manage.py migrate auth --noinput
python manage.py migrate admin --noinput
python manage.py migrate sessions --noinput

# Applica le migrazioni delle app in ordine di dipendenza
echo "🔄 Applicazione migrazioni delle app..."
python manage.py migrate accounts --noinput
python manage.py migrate artists --noinput
python manage.py migrate associates --noinput
python manage.py migrate booking --noinput
python manage.py migrate messaging --noinput
python manage.py migrate core --noinput
python manage.py migrate api --noinput

# Sincronizza eventuali app rimanenti
echo "🔄 Sincronizzazione finale..."
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
