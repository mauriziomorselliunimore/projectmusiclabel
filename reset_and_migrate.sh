#!/bin/bash

# Reset database schema
psql $DATABASE_URL -f reset_db.sql

# Apply migrations
python manage.py migrate --noinput

# Create superuser if needed (optional, decommentare se necessario)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com
