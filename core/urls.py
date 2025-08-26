from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('populate-db/', views.populate_database, name='populate_db'),
    path('clear-db/', views.clear_database, name='clear_db'),
]