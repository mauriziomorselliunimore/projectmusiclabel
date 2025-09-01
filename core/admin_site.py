from django.contrib import admin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import path
from core.views.monitor.health import health_check

class HealthCheckAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('health-check/', self.admin_view(self.health_check_view), name='admin-health-check'),
            path('control-panel/', self.admin_view(self.control_panel_view), name='control-panel'),
        ]
        return custom_urls + urls
        
    def index(self, request, extra_context=None):
        """Reindirizza la homepage admin al control panel"""
        from django.shortcuts import redirect
        return redirect('core:admin_control_panel')

    def health_check_view(self, request):
        # Riutilizziamo la funzione health_check esistente per ottenere lo stato
        health_response = health_check(request)
        health_data = health_response.content.decode('utf-8')
        
        # Renderizza il template admin con i dati
        context = {
            'title': 'Stato del Sistema',
            'health_data': health_data,
            **self.each_context(request),
        }
        
        return TemplateResponse(
            request,
            'admin/health_check.html',
            context,
        )
