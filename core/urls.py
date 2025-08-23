from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('profilo/<int:user_id>/', views.profilo, name='profilo'),
    path('ricerca/', views.ricerca, name='ricerca'),
    path('contatti/', views.contatti, name='contatti'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('artists/', include('artists.urls', namespace='artists')),
    path('demos/', include('demos.urls', namespace='demos')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile_redirect, name='profile_redirect'),
]