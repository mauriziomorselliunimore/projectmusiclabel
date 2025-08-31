#!/bin/bash

# Installa le dipendenze
pip install -r requirements.txt

# Resetta il database per l'app messaging
python manage.py migrate messaging zero

# Rimuove tutte le migrazioni esistenti dell'app messaging
rm -f messaging/migrations/0*.py

# Crea le migrazioni per ogni app senza input interattivo
python manage.py makemigrations accounts --noinput
python manage.py makemigrations core --noinput
python manage.py makemigrations artists --noinput
python manage.py makemigrations associates --noinput
python manage.py makemigrations booking --noinput
python manage.py makemigrations messaging --noinput
python manage.py makemigrations api --noinput

# Forza l'applicazione di tutte le migrazioni
python manage.py migrate --noinput

# Raccoglie i file statici
python manage.py collectstatic --noinput
