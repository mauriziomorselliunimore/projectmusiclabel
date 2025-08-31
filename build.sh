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

# Pulisci prima le migrazioni problematiche
echo "🧹 Pulizia migrazioni problematiche..."
__temp_psql << 'EOSQL'
DO $$ 
BEGIN
    -- Drop di tutte le tabelle di messaging in modo sicuro
    DROP TABLE IF EXISTS django_migrations CASCADE;
    DROP TABLE IF EXISTS messaging_notification CASCADE;
    DROP TABLE IF EXISTS messaging_message CASCADE;
    DROP TABLE IF EXISTS messaging_conversation CASCADE;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Ignoro errori di drop table: %', SQLERRM;
END $$;
EOSQL

# Crea le migrazioni per ogni app
echo "🔄 Creazione migrazioni..."
for app in core accounts artists associates booking messaging api; do
    echo "  ⚡ Migrazione per $app..."
    python manage.py makemigrations $app --noinput || echo "Nota: Nessuna migrazione necessaria per $app"
done

# Applica le migrazioni forzatamente
echo "🔄 Applicazione migrazioni forzata..."
python manage.py migrate --no-input --run-syncdb || handle_error "Migrazione database fallita"

# Migra specificamente le app principali
for app in core accounts artists associates booking messaging api; do
    echo "  ⚡ Migrazione forzata per $app..."
    python manage.py migrate $app --no-input --fake-initial || echo "Nota: Migrazione non necessaria per $app"
done
python manage.py migrate --noinput --run-syncdb

# Raccoglie i file statici
python manage.py collectstatic --noinput

# Invia i messaggi di benvenuto
python manage.py send_welcome_messages
