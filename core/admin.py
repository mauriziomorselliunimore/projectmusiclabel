
from django.contrib import admin
from django.contrib.auth import get_user_model
from .admin_site import HealthCheckAdminSite
from artists.models.artist import Artist
from associates.models import Associate
from accounts.models.profile import Profile
from booking.models import Booking
from artists.models.collaboration import CollaborationProposal

# Register Artist model
admin.site.register(Artist)

# Register Associate model
admin.site.register(Associate)

# Register Profile model
admin.site.register(Profile)

# Register Booking model
admin.site.register(Booking)

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