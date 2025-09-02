#!/bin/bash

echo "🔄 Inizializzazione reset database..."

# Reset database schema
if psql $DATABASE_URL -f reset_db.sql; then
    echo "✅ Reset database completato"
else
    echo "❌ Errore durante il reset del database"
    exit 1
fi

echo "⚡ Creazione migrazioni per ogni app..."
# Generate migrations for each app
for app in accounts artists associates booking core messaging api; do
    echo "  ⚡ Creazione migrazioni per $app..."
    python manage.py makemigrations $app
done

echo "🔄 Applicazione migrazioni..."
# Apply migrations
if python manage.py migrate --noinput; then
    echo "✅ Migrazioni applicate con successo"
else
    echo "❌ Errore durante l'applicazione delle migrazioni"
    exit 1
fi

echo "👤 Creazione superuser di default..."
# Create default superuser
DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput \
    --username admin \
    --email admin@example.com \
    && echo "✅ Superuser 'admin' creato con successo" \
    || echo "⚠️ Superuser potrebbe già esistere"

echo "🔍 Verifica integrità database..."
python manage.py check

echo "✨ Reset database completato con successo!"
