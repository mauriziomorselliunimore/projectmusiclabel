import os
from .settings import DEBUG

# Email settings con SendGrid
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # Questo deve essere letteralmente 'apikey'
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')  # La tua API key di SendGrid
DEFAULT_FROM_EMAIL = 'MyLabel <noreply@mylabel.com>'

# Verifica l'indirizzo email del mittente su SendGrid
VERIFIED_SENDER_EMAIL = os.getenv('VERIFIED_SENDER_EMAIL')

# Per il debug, usa il backend della console
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurazioni email personalizzate
EMAIL_SUBJECT_PREFIX = '[MyLabel] '
ADMINS = [('Admin', EMAIL_HOST_USER)]
MANAGERS = ADMINS

# Notifiche email
BOOKING_NOTIFICATION_EMAIL = EMAIL_HOST_USER
SUPPORT_EMAIL = EMAIL_HOST_USER
