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

La seguente struttura rappresenta l'organizzazione del backend per l'etichetta musicale. Il progetto è costruito con Django e gestito tramite Poetry.

musiclabel-backend/ ├── music_label/ # Configurazione principale Django (settings, urls, wsgi, asgi) ├── accounts/ # Gestione utenti e autenticazione ├── artists/ # Modelli e logica per gli artisti ├── associates/ # Collaboratori, ruoli e relazioni ├── core/ # Funzionalità condivise e utilities ├── pyproject.toml # Configurazione del progetto e dipendenze (Poetry) ├── manage.py # Entry point per comandi Django ├── README.md # Documentazione del progetto

## 📦 Installazione locale

Per installare il progetto in locale:

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver


📋 Per testare:
Dopo il deploy, il database sarà automaticamente popolato con:

Admin: admin / admin123
Artisti: marco_blues, sofia_pop, dj_elektro / password123
Professionisti: luca_sound, anna_producer / password123

Tutto con avatar, demo e portfolio funzionanti usando solo URL esterni! 🎉✨
