#!/bin/bash

__temp_psql() {
    psql $DATABASE_URL -v ON_ERROR_STOP=1 "$@"
}

# Installa le dipendenze
pip install -r requirements.txt

# Rimuove le tabelle problematiche in maniera sicura
__temp_psql << 'EOSQL'
DO $$ 
BEGIN
    DROP TABLE IF EXISTS messaging_notification CASCADE;
    DROP TABLE IF EXISTS messaging_message CASCADE;
    DROP TABLE IF EXISTS messaging_conversation CASCADE;
EXCEPTION WHEN OTHERS THEN
    -- Ignora eventuali errori
END $$;
EOSQL

# Crea le migrazioni per ogni app senza input interattivo
python manage.py makemigrations accounts --noinput
python manage.py makemigrations core --noinput
python manage.py makemigrations artists --noinput
python manage.py makemigrations associates --noinput
python manage.py makemigrations booking --noinput
python manage.py makemigrations messaging --noinput
python manage.py makemigrations api --noinput

# Forza l'applicazione di tutte le migrazioni
python manage.py migrate --noinput --run-syncdb

# Raccoglie i file statici
python manage.py collectstatic --noinput

# Invia i messaggi di benvenuto
python manage.py send_welcome_messages
