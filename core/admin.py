from django.contrib import admin
from .admin_site import HealthCheckAdminSite
from artists.models.collaboration import CollaborationProposal

# Register CollaborationProposal
@admin.register(CollaborationProposal)
class CollaborationProposalAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'type', 'budget', 'status', 'created_at')
    list_filter = ('status', 'type', 'mode', 'timeline')
    search_fields = ('sender__username', 'receiver__username', 'description')
    date_hierarchy = 'created_at'

# Crea una nuova istanza dell'AdminSite personalizzato
admin_site = HealthCheckAdminSite(name='admin')

# Sostituisce l'AdminSite di default con il nostro personalizzato
admin.site = admin_site