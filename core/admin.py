from django.contrib import admin
from .admin_site import HealthCheckAdminSite

# Crea una nuova istanza dell'AdminSite personalizzato
admin_site = HealthCheckAdminSite(name='admin')

# Sostituisce l'AdminSite di default con il nostro personalizzato
admin.site = admin_site