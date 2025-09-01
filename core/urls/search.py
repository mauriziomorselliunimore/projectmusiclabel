from django.urls import path
from ..views import search

app_name = 'search'

urlpatterns = [
    path('advanced/', search.advanced_search, name='advanced'),
]
