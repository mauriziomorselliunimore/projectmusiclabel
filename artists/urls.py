from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.artist_list, name='list'),
    path('<int:pk>/', views.artist_detail, name='detail'),
    path('create/', views.artist_create, name='create'),
    path('<int:pk>/edit/', views.artist_edit, name='edit'),
    path('demo/upload/', views.demo_upload, name='demo_upload'),
    path('demo/<int:pk>/delete/', views.demo_delete, name='demo_delete'),
]