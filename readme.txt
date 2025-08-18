music-label/
├── manage.py
├── requirements.txt
├── music_label/                 # Progetto principale
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                    # App autenticazione
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── artists/                     # App artisti
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── associates/                  # App associati
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── core/                        # App principale (homepage, ricerca)
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/                   # Template HTML
│   ├── base.html
│   ├── registration/
│   ├── artists/
│   ├── associates/
│   └── core/
├── static/                      # CSS, JS, immagini statiche
│   ├── css/
│   ├── js/
│   └── images/
├── media/                       # File upload (demo, foto profilo)
│   ├── demos/
│   ├── profiles/
│   └── portfolio/
└── tests/                       # Test files