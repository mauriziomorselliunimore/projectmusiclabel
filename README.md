# 🎵 MyLabel - Sistema Gestione Etichetta Discografica

## 📋 Informazioni Progetto

**Autore:** Morselli Maurizio  
**Framework:** Django 4.2.7  
**Database:** PostgreSQL (Produzione) / SQLite (Sviluppo)  
**Storage:** Cloudinary (file multimediali)  
**Deploy:** Render Cloud Platform  
**Linguaggio:** Python 3.11+  
**Repository:** [github.com/mauriziomorselliunimore/projectmusiclabel](https://github.com/mauriziomorselliunimore/projectmusiclabel)

## 🚀 Setup Progetto

### Requisiti
- Python 3.11+
- PostgreSQL (per produzione)
- Account Cloudinary (per file storage)

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

# Configurazione .env
cp .env.example .env
# Modifica .env con le tue configurazioni
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

# Host
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🌐 Deploy su Render

1. Fork del repository
2. Crea un nuovo Web Service su Render
3. Collega il repository
4. Configura le variabili d'ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `DEBUG=False`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `DJANGO_SETTINGS_MODULE=record_label.settings_production`

## 👥 Utenti Demo

### 🎸 Artisti
1. **MR Wave** (Rock)
   - Username: marco_rossi
   - Password: testpass123
   - Bio: Cantautore rock con influenze indie e alternative
   - Città: Milano

2. **LauraB** (Pop)
   - Username: laura_bianchi
   - Password: testpass123
   - Bio: Cantante pop con un tocco di soul
   - Città: Roma

3. **DJ Verde** (Electronic)
   - Username: giovanni_verdi
   - Password: testpass123
   - Bio: DJ e produttore di musica elettronica
   - Città: Torino

### 👔 Professionisti Associati
1. **Studio Sound** (Studio di Registrazione)
   - Username: studio_sound
   - Password: testpass123
   - Specializzazione: Sound Engineer
   - Skills: Recording, Mixing, Mastering, Pro Tools
   - Disponibilità: Lunedì-Venerdì 9:00-18:00
   - Tariffa: €50/ora
   - Città: Milano

2. **MasterMix** (Producer)
   - Username: master_mix
   - Password: testpass123
   - Specializzazione: Produttore Musicale
   - Skills: Production, Arrangement, Logic Pro, Ableton
   - Disponibilità: Lunedì-Mercoledì 14:00-22:00
   - Tariffa: €45/ora
   - Città: Roma

3. **Session Pro** (Session Musician)
   - Username: session_pro
   - Password: testpass123
   - Specializzazione: Chitarrista Session
   - Skills: Electric Guitar, Acoustic Guitar, Bass, Recording
   - Disponibilità: Mercoledì-Sabato 10:00-19:00
   - Tariffa: €35/ora
   - Città: Bologna

4. **Visual Arts** (Visual Artist)
   - Username: visual_arts
   - Password: testpass123
   - Specializzazione: Video Producer
   - Skills: Video Editing, Photography, After Effects, Premiere
   - Disponibilità: Martedì-Sabato 9:00-17:00
   - Tariffa: €40/ora
   - Città: Torino

### 👨‍💼 Admin
- Username: admin
- Password: admin

## 🏗️ Struttura Progetto Completa

```
record_label/
├── 📁 record_label/           # Configurazione principale
│   ├── settings.py           # Settings ottimizzati Render
│   ├── urls.py              # URL principali
│   ├── wsgi.py              # WSGI per produzione
│   └── asgi.py              # ASGI per WebSocket
├── 📁 core/                  # App principale
│   ├── views.py             # Homepage + utilities
│   ├── urls.py              # URL core
│   ├── templates/           # Template base
│   └── management/commands/  # Comandi personalizzati
├── 📁 accounts/             # Sistema autenticazione
│   ├── models.py            # Profile utente
│   ├── views.py             # Login/Register
│   ├── forms.py             # Form personalizzati
│   └── templates/           # Template auth
├── 📁 artists/              # Gestione artisti
│   ├── models.py            # Artist, Demo
│   ├── views.py             # CRUD artisti
│   ├── forms.py             # Form artisti
│   ├── admin.py             # Admin personalizzato
│   └── templates/           # Template artisti
├── 📁 associates/           # Gestione professionisti
│   ├── models.py            # Associate, PortfolioItem
│   ├── views.py             # CRUD associati
│   ├── forms.py             # Form associati
│   └── templates/           # Template associati
├── 📁 booking/              # Sistema prenotazioni
│   ├── models.py            # Booking, Availability
│   ├── views.py             # Calendario + booking
│   ├── urls.py              # URL booking
│   ├── admin.py             # Admin booking
│   └── templates/           # Template booking
├── 📁 messaging/            # Chat + notifiche
│   ├── models.py            # Message, Notification
│   ├── views.py             # Chat system
│   ├── consumers.py         # WebSocket consumers
│   ├── forms.py             # Form messaggi
│   └── templates/           # Template messaging
├── 📁 api/                  # REST API
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API endpoints
│   └── urls.py              # URL API
├── 📁 templates/            # Template globali
│   └── base.html            # Template base
├── 📁 static/               # File statici
├── 📁 staticfiles/          # File statici produzione
├── requirements.txt         # Dipendenze Python
└── manage.py               # Django manage
```

---
## 💾 Setup Database e Popolamento

### 🗃️ Inizializzazione Automatica

Il sistema è configurato per auto-inizializzarsi al primo deploy. Il comando `populate_db` crea:

1. **Superuser di amministrazione**
   - Username: admin
   - Password: admin

2. **Artisti demo**
   - MR Wave (Rock)
     * Username: marco_rossi
     * Password: testpass123
   - LauraB (Pop)
     * Username: laura_bianchi
     * Password: testpass123
   - DJ Verde (Electronic)
     * Username: giovanni_verdi
     * Password: testpass123

3. **Professionisti demo**
   - Studio Sound (Studio di Registrazione)
     * Username: studio_sound
     * Password: testpass123
   - Talent Scout Agency (Management)
     * Username: talent_scout
     * Password: testpass123
   - PromoEvents (Promoter)
     * Username: promo_events
     * Password: testpass123

---

## 🎯 Funzionalità Principali

### 🎼 Gestione Audio
- Upload demo tramite file (max 5MB) o link esterni
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
- **Primary:** #ff2e88 (Magenta)
- **Secondary:** #d72660 (Dark Magenta)  
- **Background:** #000000 (Black)
- **Card Background:** #1b1b1b (Dark Gray)
- **Text:** #ffffff (White)

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

```bash
# Sviluppo locale
python manage.py runserver
python manage.py populate_db
python manage.py shell

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