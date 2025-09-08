# Register Artist model
from artists.models.artist import Artist
admin.site.register(Artist)

# Register Associate model
from associates.models import Associate
admin.site.register(Associate)

# Register Profile model
from accounts.models.profile import Profile
admin.site.register(Profile)

# Register Booking model
from booking.models import Booking
admin.site.register(Booking)

from django.contrib import admin
from django.contrib.auth import get_user_model
from .admin_site import HealthCheckAdminSite
from artists.models.collaboration import CollaborationProposal

# Register CollaborationProposal
@admin.register(CollaborationProposal)
class CollaborationProposalAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'type', 'budget', 'status', 'created_at')
    list_filter = ('status', 'type', 'mode', 'timeline')
    search_fields = ('sender__username', 'receiver__username', 'description')
    date_hierarchy = 'created_at'

# Register User model
User = get_user_model()
admin.site.register(User)

# Crea una nuova istanza dell'AdminSite personalizzato
admin_site = HealthCheckAdminSite(name='admin')

# Sostituisce l'AdminSite di default con il nostro personalizzato
admin.site = admin_site