from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('populate-db/', views.populate_database, name='populate_db'),
    path('clear-db/', views.clear_database, name='clear_db'),
    path('create-admin/', views.create_superuser_render, name='create_admin'),
    path('render-status/', views.render_status, name='render_status'),
]