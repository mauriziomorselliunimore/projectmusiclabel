from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models.auth_logs import LoginLog

@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    """Log dei login riusciti"""
    if request:
        # Determina il tipo di dispositivo dal user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_type = 'Mobile' if 'Mobile' in user_agent else 'Desktop'
        if 'Tablet' in user_agent:
            device_type = 'Tablet'

        LoginLog.objects.create(
            user=user,
            ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'),
            user_agent=user_agent,
            success=True,
            device_type=device_type
        )

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """Log dei tentativi di login falliti"""
    if request and 'username' in credentials:
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=credentials['username'])
        except User.DoesNotExist:
            user = None

        LoginLog.objects.create(
            user=user,  # Può essere None
            ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=False,
            device_type='Unknown'
        )
