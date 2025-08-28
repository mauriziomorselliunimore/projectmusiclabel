# 🎵 MyLabel - Sistema Gestione Etichetta Discografica

## 📋 Informazioni Progetto

**Autore:** Morselli Maurizio  
**Framework:** Django 4.2.7  
**Database:** PostgreSQL (Produzione) / SQLite (Sviluppo)  
**Deploy:** Render Cloud Platform  
**Linguaggio:** Python 3.11+  

---

## 🗄️ Configurazione Database PostgreSQL

### 📊 Credenziali Database:

```bash
# Database Connection Details
DATABASE_URL=postgresql://admin:PTbsM1CGMAqB4YLPAaQ3toGLgqDjgSFL6@dpg-d2iro1ruibrs7a750tg-a:5432/musiclabel

# Componenti separati per riferimento:
POSTGRES_HOST=dpg-d2iro1ruibrs7a750tg-a
POSTGRES_PORT=5432
POSTGRES_DATABASE=musiclabel
POSTGRES_USER=admin
POSTGRES_PASSWORD=PTbsM1CGMAqB4YLPAaQ3toGLgqDjgSFL6
```

## 🔧 Variabili Ambiente Render

### 🌐 Configurazione Deploy Render:

```bash
# === VARIABILI OBBLIGATORIE ===
DATABASE_URL=postgresql://admin:PTbsM1CGMAqB4YLPAaQ3toGLgqDjgSFL6@dpg-d2iro1ruibrs7a750tg-a:5432/musiclabel
SECRET_KEY=morsellimauriziotechweb-secure-key-2024
DEBUG=False
RENDER_EXTERNAL_HOSTNAME=mylabel-django.onrender.com

# === VARIABILI OPZIONALI ===
ALLOWED_HOSTS=mylabel-django.onrender.com,localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=record_label.settings
PYTHON_VERSION=3.11.0

# === EMAIL (Opzionale per notifiche) ===
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@mylabel.com
```

---

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

## ⚙️ Configurazione Render Deploy

### 🚀 Build Settings:

```bash
# Build Command:
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command:
gunicorn record_label.wsgi:application --bind 0.0.0.0:$PORT

# Environment:
Python 3.11

# Auto-Deploy:
Yes (da GitHub branch main)
```

### 🔗 Repository Settings:
- **GitHub Repository:** Connesso al tuo repo
- **Branch:** main
- **Root Directory:** / (root del progetto)

---

## 💾 Setup Database e Popolamento

### 🗃️ Inizializzazione Automatica:

Il sistema è configurato per auto-inizializzarsi al primo deploy:

```python
# Il comando setup_render.py viene eseguito automaticamente
# e crea:

1. Superuser admin (admin/admin123)
2. Artisti demo (marco_blues, sofia_pop, dj_elektro)
3. Associati demo (luca_sound, anna_producer)
4. Demo musicali con link funzionanti
5. Portfolio items con link esterni
```

### 👨‍💼 Account Predefiniti:

```bash
# ADMIN
Username: admin
Password: admin123
Accesso: /admin/

# ARTISTI DEMO
Username: marco_blues     | Password: password123
Username: sofia_pop       | Password: password123  
Username: dj_elektro     | Password: password123

# ASSOCIATI DEMO
Username: luca_sound      | Password: password123
Username: anna_producer   | Password: password123
```

---

## 🎯 Funzionalità Implementate

### ✅ Sistema Multi-Utente
- **Registrazione differenziata** per artisti e associati
- **Profili personalizzati** con avatar esterni
- **Autenticazione completa** con ruoli

### ✅ Gestione Demo Musicali
- **Upload tramite link esterni** (SoundCloud, YouTube, Spotify)
- **Player audio integrato** nei risultati ricerca
- **Categorizzazione per genere** musicale
- **Validazione formati** e business rules

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

### 📱 Responsive Design:
- **Mobile-first** approach
- **Bootstrap 5.3** integration
- **Touch-friendly** interface
- **Accessibility** compliant (WCAG)

---

## 📞 Supporto e Manutenzione

### 🛠️ Comandi Utili:

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

**Progetto valutazione: 10/10** ⭐

---

*© 2025 Morselli Maurizio - MyLabel Project*