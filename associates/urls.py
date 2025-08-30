from django.urls import path
from . import views

app_name = 'associates'

urlpatterns = [
    path('', views.associate_list, name='list'),
    path('<int:pk>/', views.associate_detail, name='detail'),
    path('create/', views.associate_create, name='create'),
    path('<int:pk>/edit/', views.associate_edit, name='edit'),
    path('portfolio/add/', views.portfolio_add, name='portfolio_add'),
    path('portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),
    path('quick-message/', views.quick_message, name='quick_message'),
]