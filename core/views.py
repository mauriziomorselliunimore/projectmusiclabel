from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from artists.models import Artist
from associates.models import Associate
from django.contrib.auth import get_user_model



def profilo(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'profilo.html', {'user': user})

def ricerca(request):
    risultati = []  # Sostituisci con la tua logica di ricerca
    return render(request, 'ricerca.html', {'risultati': risultati})

def home(request):
    return render(request, 'home.html')
