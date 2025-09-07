from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.openapi import AutoSchema
from rest_framework import permissions

SPECTACULAR_SETTINGS = {
    'TITLE': 'MyLabel API',
    'DESCRIPTION': """
    API dell'applicazione MyLabel per la gestione di artisti, professionisti e recensioni.
    
    ## Autenticazione
    
    L'API richiede autenticazione per la maggior parte delle operazioni. Usa il token di autenticazione
    nell'header `Authorization: Token <your-token>`.
    
    ## Rate Limiting
    
    Le richieste sono limitate a:
    - 100 richieste/ora per utenti autenticati
    - 20 richieste/ora per utenti non autenticati
    
    ## Endpoints Principali
    
    * `/api/artists/` - Gestione artisti
    * `/api/associates/` - Gestione professionisti
    * `/api/reviews/` - Gestione recensioni
    * `/api/bookings/` - Gestione prenotazioni
    
    ## Formati
    
    L'API supporta JSON e form-data per gli upload di file.
    """,
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'MyLabel Support',
        'url': 'https://www.mylabel.com',
        'email': 'support@mylabel.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
}

urlpatterns = [
    # Schema URLs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
