#!/bin/bash

# Installa le dipendenze necessarie
pip install django-cors-headers

# Crea un file Python temporaneo per configurare l'admin
cat > setup_admin.py << EOL
from django.contrib.auth.models import User
from accounts.models import Profile

# Cerca l'utente admin o crealo se non esiste
user, created = User.objects.get_or_create(username='admin')

# Imposta le credenziali e i permessi
user.set_password('admin123')  # Imposta la password
user.is_staff = True          # Dà accesso all'admin panel
user.is_superuser = True      # Dà tutti i permessi
user.email = 'admin@example.com'
user.save()

# Crea o aggiorna il profilo
profile, created = Profile.objects.get_or_create(user=user)
profile.user_type = 'associate'  # o 'artist' in base alle necessità
profile.save()

print('Admin user configurato con successo!')
EOL

# Esegui lo script Python
python manage.py shell < setup_admin.py

# Rimuovi il file temporaneo
rm setup_admin.py

echo "Setup completato!"
