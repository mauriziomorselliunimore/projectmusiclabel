from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from .models.auth_logs import LoginLog

@login_required
def security_settings(request):
    """Vista per le impostazioni di sicurezza dell'account"""
    recent_logins = LoginLog.objects.filter(
        user=request.user,
        success=True
    ).order_by('-timestamp')[:5]

    failed_attempts = LoginLog.objects.filter(
        user=request.user,
        success=False
    ).count()

    context = {
        'recent_logins': recent_logins,
        'failed_attempts': failed_attempts,
    }
    return render(request, 'accounts/security_settings.html', context)

@login_required
def login_activity(request):
    """Vista per visualizzare lo storico degli accessi"""
    logs = LoginLog.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(logs, 20)  # 20 logs per pagina
    
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    
    context = {
        'logs': logs_page,
    }
    return render(request, 'accounts/login_activity.html', context)
