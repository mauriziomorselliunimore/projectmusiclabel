from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    verbose_name = 'Sistema Messaggistica'

    def ready(self):
        import messaging.signals  # Importa i segnali quando l'app è pronta