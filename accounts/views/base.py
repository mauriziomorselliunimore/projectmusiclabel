from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import CustomUserCreationForm, ProfileForm
from ..models.profile import Profile
from core.email import send_welcome_email

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile
            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type']
            )
            # Invia email di benvenuto
            send_welcome_email(user)
            
            login(request, user)
            messages.success(request, 'Registrazione completata con successo!')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
