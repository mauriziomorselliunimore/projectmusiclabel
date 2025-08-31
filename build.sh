#!/bin/bash

# Installa le dipendenze
pip install -r requirements.txt

# Crea le migrazioni per ogni app senza input interattivo
python manage.py makemigrations accounts --noinput
python manage.py makemigrations core --noinput
python manage.py makemigrations artists --noinput
python manage.py makemigrations associates --noinput
python manage.py makemigrations booking --noinput
python manage.py makemigrations messaging --noinput
python manage.py makemigrations api --noinput

# Applica le migrazioni
python manage.py migrate

# Raccoglie i file statici
python manage.py collectstatic --noinput
