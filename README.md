# 🎵 MyLabel - Sistema Gestione Etichetta Discografica

## 📋 Informazioni Progetto

**Autore:** Morselli Maurizio  
**Framework:** Django 4.2.7  
**Database:** PostgreSQL (Produzione) / SQLite (Sviluppo)  
**Storage:** Cloudinary (file multimediali)  
**Cache:** Redis (messaggistica real-time e caching)  
**Deploy:** Render Cloud Platform  
**Linguaggio:** Python 3.11+  
**Repository:** [github.com/mauriziomorselliunimore/projectmusiclabel](https://github.com/mauriziomorselliunimore/projectmusiclabel)

## 💡 Caratteristiche Principali

- **Sistema di Messaggistica Real-time**: Chat in tempo reale tra artisti e professionisti
- **Booking System**: Gestione prenotazioni con calendario e disponibilità
- **Dashboard Amministrativa**: Interfaccia personalizzata per gestire utenti e contenuti
- **Sistema di Review**: Recensioni e feedback per artisti e professionisti
- **API REST**: Documentazione completa con drf-spectacular
- **WebSocket**: Notifiche in tempo reale con Django Channels
- **Storage Cloud**: Gestione file multimediali con Cloudinary
- **Performance**: Caching con Redis e ottimizzazioni database
- **Sicurezza**: Protezione CSRF, XSS, e rate limiting

## 🚀 Setup Progetto

### Requisiti
- Python 3.11+
- PostgreSQL (per produzione)
- Redis (per WebSocket e caching)
- Account Cloudinary (per file storage)
- FFmpeg (per processamento audio)

## 👥 Credenziali Demo

### 👨‍💼 Admin
- Username: `admin`
- Password: `admin123`
- Email: admin@example.com

### 🎤 Artisti
1. **Blues Marco** (Chitarrista Blues)
   - Username: `marco_blues`
   - Password: `password123`
   - Email: marco@example.com
   
2. **Sofia B** (Cantante Pop)
   - Username: `sofia_pop`
   - Password: `password123`
   - Email: sofia@example.com
   
3. **DJ Elektro** (Producer EDM)
   - Username: `dj_elektro`
   - Password: `password123`
   - Email: alessandro@example.com

### 🎛️ Professionisti
1. **Luca Ferrari** (Sound Engineer)
   - Username: `luca_sound`
   - Password: `password123`
   - Email: luca@example.com
   
2. **Anna Romano** (Music Producer)
   - Username: `anna_producer`
   - Password: `password123`
   - Email: anna@example.com

*Nota: Tutti gli utenti demo utilizzano la stessa password: `password123`*

### 🔧 Installazione Locale
```bash
# Clone repository
git clone https://github.com/mauriziomorselliunimore/projectmusiclabel.git
cd projectmusiclabel

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
pip install -r requirements_audio.txt  # Per processamento audio

# Configurazione .env
cp .env.example .env
# Modifica .env con le tue configurazioni

# Avvia Redis (necessario per WebSocket e caching)
# Windows: Avvia Redis da Windows Subsystem for Linux (WSL)
# Linux/Mac: sudo service redis-server start
```

### ⚙️ Variabili Ambiente (.env)
```properties
# Database
DATABASE_URL=your_database_url

# Security
SECRET_KEY=your_secret_key
DEBUG=True  # False in produzione

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Redis
REDIS_URL=redis://localhost:6379/0

# Host
ALLOWED_HOSTS=localhost,127.0.0.1

# Email con SendGrid (configurato ma non ancora testato)
SENDGRID_API_KEY=your_sendgrid_api_key
DEFAULT_FROM_EMAIL=your_verified_sender@yourdomain.com

# Email Fallback (SMTP alternativo)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_app_password
```

## 🌐 Deploy su Render

1. Fork del repository
2. Crea un nuovo Web Service su Render
3. Collega il repository
4. Configura le variabili d'ambiente come nel file .env
5. Aggiungi il build command:
```bash
./build.sh
```
6. Aggiungi lo start command:
```bash
daphne record_label.asgi:application -b 0.0.0.0 -p $PORT
```
7. Configura Redis:
   - Aggiungi un Redis service su Render
   - Collega il Redis service al Web service

### 🔄 Reset Database e Migrazione (se necessario)
```bash
./reset_and_migrate.sh
```

### 👤 Setup Admin (se necessario)
```bash
./setup_admin.sh
```

## ⚙️ Features Tecniche

### 💬 Sistema di Messaggistica
- Chat in tempo reale con WebSocket
- Notifiche push per nuovi messaggi
- Indicatori di lettura
- Supporto emoji e markdown
- Archiviazione conversazioni

### 📅 Sistema di Booking
- Gestione disponibilità settimanale
- Prenotazioni one-time e ricorrenti
- Calendario interattivo
- Notifiche automatiche
- Sistema di conferma/rifiuto

### 👤 Profili Utente
- Profili specializzati per artisti e professionisti
- Portfolio multimediale
- Sistema di rating e recensioni
- Badge e verifiche
- Gestione privacy

### ⚡ Performance
- Caching multi-livello con Redis
- Ottimizzazione query database
- Lazy loading immagini
- Compressione asset statici
- Rate limiting API

### 🔒 Sicurezza
- Autenticazione token-based
- Protezione CSRF e XSS
- Rate limiting per IP
- Validazione input
- Sanitizzazione output

### 📧 Sistema Email
- Integrazione SendGrid (configurata)
- Template email personalizzabili
- Fallback SMTP configurabile
- Code di invio asincrone
- Tracciamento delivery (quando attivo)

## 📚 Documentazione API

La documentazione API completa è disponibile all'endpoint `/api/schema/swagger-ui/`

Principali endpoint:
- `/api/artists/`: Gestione artisti
- `/api/associates/`: Gestione professionisti
- `/api/bookings/`: Gestione prenotazioni
- `/api/reviews/`: Sistema recensioni
- `/api/messages/`: Sistema messaggistica

## 🏗️ Struttura Progetto Completa

```
projectmusiclabel/
├── 📁 record_label/          # Configurazione principale
│   ├── settings.py          # Settings principali
│   ├── settings_api.py      # Config API
│   ├── settings_cache.py    # Config Redis
│   ├── settings_email.py    # Config Email
│   ├── settings_media.py    # Config Media
│   ├── settings_production.py # Settings prod
│   ├── urls.py             # URL principali
│   ├── wsgi.py             # WSGI config
│   └── asgi.py             # ASGI per WebSocket
├── 📁 core/                 # App principale
│   ├── admin_site.py       # Admin personalizzato
│   ├── admin.py            # Admin models
│   ├── cache.py            # Cache utils
│   ├── decorators.py       # Custom decorators
│   ├── email.py            # Email handlers
│   ├── metrics.py          # Metriche sistema
│   ├── middleware.py       # Middleware custom
│   ├── models.py           # Core models
│   ├── storage.py          # Storage handlers
│   ├── urls/               # URL suddivisi
│   ├── views/              # Views suddivise
│   ├── templates/          # Template base
│   └── management/commands/ # Comandi custom
├── 📁 accounts/            # Sistema auth
│   ├── admin.py           # Admin utenti
│   ├── forms.py           # Form auth
│   ├── models/            # Models suddivisi
│   │   ├── auth_logs.py   # Log accessi
│   │   └── profile.py     # Profili utente
│   ├── signals.py         # Signals auth
│   ├── views/             # Views suddivise
│   │   ├── base.py       # Views base
│   │   └── security.py   # Security views
│   └── templates/         # Template auth
├── 📁 artists/            # Gestione artisti
│   ├── admin.py          # Admin artisti
│   ├── forms.py          # Form artisti
│   ├── models/           # Models suddivisi
│   │   ├── artist.py     # Model artista
│   │   ├── collaboration.py # Collaborazioni
│   │   ├── constants.py  # Costanti
│   │   └── demo.py       # Demo musicali
│   ├── utils.py          # Utilities
│   ├── views/            # Views suddivise
│   └── templates/        # Template artisti
├── 📁 associates/         # Gestione professionisti
│   ├── admin.py          # Admin associati
│   ├── forms.py          # Form associati
│   ├── models.py         # Models associati
│   ├── views.py          # Views associati
│   └── templates/        # Template associati
├── 📁 booking/           # Sistema prenotazioni
│   ├── admin.py          # Admin booking
│   ├── forms.py          # Form booking
│   ├── models.py         # Models booking
│   ├── views.py          # Views booking
│   └── templates/        # Template booking
├── 📁 messaging/         # Chat + notifiche
│   ├── admin.py          # Admin messaggi
│   ├── apps.py          # Config app
│   ├── consumers.py      # WebSocket consumers
│   ├── context_processors.py # Context custom
│   ├── forms.py         # Form messaggi
│   ├── models/          # Models suddivisi
│   ├── routing.py       # Routing WebSocket
│   ├── signals.py       # Signals messaggi
│   ├── utils.py         # Utilities
│   ├── views.py         # Views principali
│   └── templates/       # Template messaggi
├── 📁 reviews/          # Sistema recensioni
│   ├── admin.py         # Admin recensioni
│   ├── cache.py         # Cache recensioni
│   ├── forms.py         # Form recensioni
│   ├── models.py        # Models recensioni
│   ├── views.py         # Views recensioni
│   └── templates/       # Template recensioni
├── 📁 api/              # REST API
│   ├── apps.py         # Config API
│   ├── docs.py         # Documentazione
│   ├── serializers.py  # DRF serializers
│   ├── throttling.py   # Rate limiting
│   ├── urls.py         # URL API
│   └── views/          # Views API
├── 📁 docs/             # Documentazione
│   ├── setup_guide.md  # Guida setup
│   └── technical_overview.md # Overview tecnico
├── 📁 static/          # File statici dev
├── 📁 staticfiles/     # File statici prod
├── 📁 settings/        # Settings aggiuntivi
├── 📁 test/            # Test aggiuntivi
├── .env               # Variabili ambiente
├── .env.example       # Template env
├── build.sh           # Script build
├── manage.py          # Django manage
├── render.yaml        # Config Render
├── requirements.txt   # Dipendenze base
├── requirements_audio.txt # Dipendenze audio
├── reset_and_migrate.sh  # Script reset DB
├── reset_db.sql         # SQL reset
└── setup_admin.sh       # Script setup admin
```

---
## 💾 Setup Database e Popolamento

### 🗃️ Inizializzazione Automatica

Il sistema è configurato per auto-inizializzarsi al primo deploy. Usa lo script `setup_admin.sh` o il comando `python manage.py setup_render` per:

1. Applicare le migrazioni del database
2. Creare il superuser amministratore
3. Popolare il database con:
   - Profili artisti demo
   - Profili professionisti demo
   - Disponibilità di esempio
   - Demo con URL esterni funzionanti
   - Portfolio items di esempio

Gli account demo creati sono quelli elencati nella sezione "Credenziali Demo" all'inizio di questo documento.

---

## 🎯 Funzionalità Principali

### 🎼 Gestione Audio
- Upload demo tramite file (max 10MB) o link esterni
- Supporto per piattaforme: SoundCloud, YouTube, Spotify
- Player audio integrato con waveform
- Gestione automatica dello storage con Cloudinary

### 👥 Sistema Multi-Utente
- Registrazione differenziata (Artisti/Professionisti)
- Profili personalizzati
- Sistema di autenticazione completo

### 📅 Sistema Booking
- Calendario disponibilità
- Prenotazione sessioni
- Prevenzione conflitti orario
- Notifiche automatiche

### 🔍 Ricerca Avanzata
- Filtri per genere musicale
- Ricerca per competenze
- Filtri per disponibilità e tariffe
- Player integrato nei risultati

### 💬 Messaging System
- Chat interna
- Notifiche in tempo reale
- Gestione conversazioni

### ✅ Sistema Booking Avanzato
- **Calendario integrato** per prenotazioni
- **Prevenzione conflitti orari** automatica
- **Workflow approvazione** (pending → confirmed → completed)
- **Calcolo costi automatico** basato su tariffe orarie

### ✅ Ricerca e Filtri
- **Motore ricerca avanzato** con filtri combinati
- **Ricerca per genere, competenze, località**
- **Filtri disponibilità e fascia prezzo**
- **Paginazione ottimizzata**

### ✅ Sistema Messaggistica
- **Chat real-time** tra utenti
- **Notifiche push** per nuovi messaggi
- **Sistema conversazioni** organizzato
- **WebSocket integration** per tempo reale

### ✅ REST API Completa
- **Endpoints per tutti i modelli** (Artists, Associates, Demos, Bookings)
- **Autenticazione token-based**
- **Paginazione e filtri** automatici
- **Documentazione API** integrata

### ✅ Admin Interface Personalizzata
- **Dashboard con statistiche** dettagliate  
- **Gestione contenuti** avanzata
- **Moderazione** artisti e associati
- **Batch operations** per efficienza

---

## 🔒 Sicurezza e Performance

### 🛡️ Security Features:
- **HTTPS enforcement** in produzione
- **CSRF protection** su tutti i form
- **SQL injection protection** tramite ORM Django
- **XSS protection** con template escaping
- **Rate limiting** per API endpoints

### ⚡ Performance Optimizations:
- **Database indexing** su campi chiave
- **Query optimization** con select_related
- **Static files caching** con WhiteNoise
- **CDN ready** per file statici
- **Pagination** per dataset grandi

---

## 🧪 Testing e Quality Assurance

### ✅ Test Coverage:
- **Unit tests** per tutti i modelli
- **Integration tests** per workflow booking
- **Form validation tests** per business rules
- **API endpoint tests** per REST interface

### 📊 Monitoring:
- **Django Debug Toolbar** in sviluppo
- **Logging configurato** per produzione
- **Error tracking** con stack traces
- **Performance monitoring** database queries

---

## 🚀 Deploy Checklist

### ✅ Pre-Deploy:
- [x] Database PostgreSQL configurato
- [x] Variabili ambiente impostate
- [x] Static files configurati
- [x] HTTPS settings abilitati
- [x] Email backend configurato

### ✅ Post-Deploy:
- [x] Migrazioni eseguite automaticamente
- [x] Static files raccolti
- [x] Superuser creato
- [x] Database popolato con dati demo
- [x] SSL certificato attivo

---

## 📱 Endpoints API Principali

### 🎤 Artists:
```
GET  /api/artists/          # Lista artisti
GET  /api/artists/{id}/     # Dettaglio artista
GET  /api/demos/            # Lista demo pubbliche
```

### 🔧 Associates:
```
GET  /api/associates/       # Lista professionisti
GET  /api/associates/{id}/  # Dettaglio professionista
```

### 📅 Bookings:
```
GET  /api/my-bookings/      # I miei booking (auth required)
GET  /api/bookings/         # Lista booking (auth required)
```

### 💬 Messaging:
```
GET  /api/messages/         # I miei messaggi (auth required)
GET  /api/notifications/    # Le mie notifiche (auth required)
POST /api/notifications/mark-read/  # Segna come lette
```

### 📊 Statistics:
```
GET  /api/stats/            # Statistiche globali
GET  /api/search/?q=term    # Ricerca globale
```

---

## 🎨 Design e UX

### 🌈 Color Scheme:
- **Primary:** #2e86ff (Blu vivace)
- **Secondary:** #ffbe2e (Giallo acceso)
- **Background:** #181818 (Nero/grigio scuro)
- **Card Background:** #23272a (Grigio medio)
- **Text:** #f5f5f5 (Bianco caldo)

### 📱 Responsive Design
- **Mobile-first** approach
- **Bootstrap 5.3** integration
- **Touch-friendly** interface
- **Accessibility** compliant (WCAG)

---

## 📞 Supporto e Manutenzione

### 🛠️ Comandi Utili
```bash
# Sviluppo locale
python -m venv venv               # Crea ambiente virtuale
.\venv\Scripts\activate           # Attiva ambiente virtuale (Windows)
source venv/bin/activate         # Attiva ambiente virtuale (Linux/Mac)
pip install -r requirements.txt   # Installa dipendenze

# Setup iniziale
python manage.py migrate         # Applica migrazioni
python manage.py populate_db     # Popola database con dati demo
python manage.py runserver       # Avvia server di sviluppo

# Produzione
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```

### 🔍 Debug Commands:
```bash
# Verifica configurazione
python manage.py check --deploy

# Test database connection  
python manage.py dbshell

# View migrations
python manage.py showmigrations
```

---

## 📈 Metrics e KPIs

### 📊 Dashboard Metrics:
- **Total Artists:** Numero artisti registrati
- **Total Associates:** Numero professionisti attivi  
- **Total Demos:** Demo pubbliche disponibili
- **Total Bookings:** Prenotazioni effettuate
- **Active Conversations:** Chat attive

### 🎯 Business KPIs:
- **User Retention:** Utenti attivi mensili
- **Booking Conversion:** Richieste → Confermate
- **Platform Growth:** Nuove registrazioni
- **Content Quality:** Demo con link funzionanti

---

## 🏆 Conclusioni

**MyLabel** è un sistema completo e professionale per la gestione di un'etichetta discografica che implementa tutte le funzionalità richieste con un alto livello di qualità tecnica e user experience.

Il progetto dimostra competenze avanzate in Django e rappresenta una soluzione reale per il settore musicale, combinando tecnologie moderne con business logic significativa.

---

*© 2025 Morselli Maurizio - MyLabel Project*
