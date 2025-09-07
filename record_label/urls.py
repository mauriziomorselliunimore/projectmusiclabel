"""
URL configuration for record_label project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core app (homepage)
    path('', include('core.urls', namespace='core')),
    
    # Authentication
    path('accounts/', include('accounts.urls', namespace='accounts')),
    
    # Main features
    path('artists/', include('artists.urls', namespace='artists')),
    path('associates/', include('associates.urls', namespace='associates')),
    path('booking/', include('booking.urls', namespace='booking')),
    path('messaging/', include('messaging.urls', namespace='messaging')),  # ✅ CORRETTO: messaging/ non messages/
    path('reviews/', include('reviews.urls', namespace='reviews')),
    
    # API
    path('api/', include('api.urls', namespace='api')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site headers
admin.site.site_header = "MyLabel Administration"
admin.site.site_title = "MyLabel Admin"
admin.site.index_title = "Benvenuto nel pannello di amministrazione MyLabel"