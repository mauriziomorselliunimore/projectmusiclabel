from django.urls import path
from . import views
from .views import proposals

app_name = 'artists'

urlpatterns = [
    path('', views.artist_list, name='list'),
    path('<int:pk>/', views.artist_detail, name='detail'),
    path('create/', views.artist_create, name='create'),
    path('profile/', views.artist_profile, name='profile'),
    path('<int:pk>/edit/', views.artist_edit, name='edit'),
    path('demo/upload/', views.demo_upload, name='demo_upload'),
    path('demo/<int:pk>/delete/', views.demo_delete, name='demo_delete'),
    path('quick-message/', views.quick_message, name='quick_message'),
    
    # Proposals
    path('proposals/', proposals.proposal_list, name='proposals'),
    path('proposals/<int:proposal_id>/update-status/', proposals.update_proposal_status, name='update_proposal_status'),
    path('proposals/<int:proposal_id>/counter-proposal/', proposals.counter_proposal, name='counter_proposal'),
]