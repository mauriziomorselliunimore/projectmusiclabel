from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from .models.profile import Profile
import logging

from core.email import send_welcome_email

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Create profile
                Profile.objects.create(
                    user=user,
                    user_type=form.cleaned_data['user_type']
                )
                # Send welcome email
                try:
                    send_welcome_email(user)
                    messages.success(request, 'Account creato con successo!')
                except Exception as e:
                    messages.warning(request, 'Account creato con successo, ma non è stato possibile inviare l\'email di benvenuto.')
                    logger.error(f"Errore nell'invio dell'email di benvenuto per l'utente {user.email}: {str(e)}")
                return redirect('core:home')
            except Exception as e:
                logger.error(f"Errore nella creazione dell'account: {str(e)}")
                messages.error(request, 'Si è verificato un errore durante la creazione dell\'account. Riprova più tardi.')
                return render(request, 'registration/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_edit(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
    except Exception as e:
        messages.error(request, 'Error accessing profile. Please try again.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, 'Error updating profile. Please try again.')
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to update profile: {e}")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def profile_view(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        return render(request, 'accounts/profile.html', {'profile': profile})
    except Exception as e:
        messages.error(request, 'Errore nell\'accesso al profilo. Riprova più tardi.')
        logger.error(f"Errore nell'accesso al profilo dell'utente {request.user.email}: {str(e)}")
        return redirect('core:home')