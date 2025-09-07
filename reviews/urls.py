from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:user_id>/', views.create_review, name='create'),
    path('edit/<int:review_id>/', views.edit_review, name='edit'),
    path('delete/<int:review_id>/', views.delete_review, name='delete'),
    path('user/<int:user_id>/', views.user_reviews, name='user_reviews'),
]
