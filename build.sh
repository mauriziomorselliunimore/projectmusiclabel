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

# Crea le migrazioni per messaging (con il nuovo campo message)
echo "🔄 Creazione migrazioni per messaging..."
python manage.py makemigrations messaging --noinput || echo "Nota: Nessuna migrazione necessaria per messaging"

# Applica le migrazioni in ordine corretto
echo "🔄 Applicazione migrazioni in ordine..."
python manage.py migrate contenttypes --noinput
python manage.py migrate auth --noinput
python manage.py migrate admin --noinput
python manage.py migrate sessions --noinput
python manage.py migrate messaging --noinput
python manage.py migrate --noinput
python manage.py migrate --noinput --run-syncdb

# Raccoglie i file statici
python manage.py collectstatic --noinput

# Invia i messaggi di benvenuto
python manage.py send_welcome_messages
