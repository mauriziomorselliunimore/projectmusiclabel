from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('profilo/<int:user_id>/', views.profilo, name='profilo'),
    path('ricerca/', views.ricerca, name='ricerca'),
]