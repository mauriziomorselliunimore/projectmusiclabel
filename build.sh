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

# Rimuove le tabelle problematiche in maniera sicura
echo "🗑️ Pulizia database..."
__temp_psql << 'EOSQL'
DO $$ 
BEGIN
    DROP TABLE IF EXISTS messaging_notification CASCADE;
    DROP TABLE IF EXISTS messaging_message CASCADE;
    DROP TABLE IF EXISTS messaging_conversation CASCADE;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Ignoro errori di drop table: %', SQLERRM;
END $$;
EOSQL

# Crea le migrazioni per ogni app
echo "🔄 Creazione migrazioni..."
for app in accounts core artists associates booking messaging api; do
    echo "  ⚡ Migrazione per $app..."
    python manage.py makemigrations $app --noinput || handle_error "Migrazione fallita per $app"
done

# Forza l'applicazione di tutte le migrazioni
python manage.py migrate --noinput --run-syncdb

# Raccoglie i file statici
python manage.py collectstatic --noinput

# Invia i messaggi di benvenuto
python manage.py send_welcome_messages
