# 🎵 Music Label Backend

Backend per la gestione di un'etichetta musicale, sviluppato con **Django** e gestito tramite **Poetry**. Questo progetto fornisce API per la gestione di artisti, account, collaboratori e contenuti musicali.
Questo progetto è distribuito sotto licenza MIT. Sentiti libero di usarlo, modificarlo e condividerlo.

## 🚀 Tecnologie utilizzate

- Python 3.13
- Django 4.2
- PostgreSQL
- Poetry per la gestione delle dipendenze
- Gunicorn per il deployment
- Whitenoise per la gestione dei file statici
- Django Debug Toolbar per lo sviluppo
- Psycopg2-binary per la connessione al database

## 📦 STRUTTURA PROGETTO 

musiclabel-backend/
├── music_label/         # Configurazione principale Django
├── accounts/            # Gestione utenti
├── artists/             # Gestione artisti
├── associates/          # Collaboratori e ruoli
├── core/                # Funzionalità condivise
├── pyproject.toml       # Configurazione Poetry
├── manage.py            # Entry point Django
├── README.md            # Questo file

## 📦 Installazione locale

Per installare il progetto in locale:

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
