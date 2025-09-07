from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from messaging.models import Message
from booking.models import Booking
from datetime import datetime
import json

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@user_passes_test(is_admin)
def get_user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Get user statistics
        message_count = Message.objects.filter(sender=user).count()
        booking_count = Booking.objects.filter(user=user).count()
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'date_joined': user.date_joined.strftime('%d/%m/%Y'),
            'last_login': user.last_login.strftime('%d/%m/%Y %H:%M') if user.last_login else 'Mai',
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'avatar': user.profile.avatar.url if user.profile.avatar else None,
            'user_type': user.profile.get_user_type_display(),
            'role': 'Superadmin' if user.is_superuser else 'Staff' if user.is_staff else user.profile.get_user_type_display(),
            'stats': {
                'messages': message_count,
                'bookings': booking_count,
            }
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Utente non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_user(request, user_id):
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        
        # Update user fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.is_active = data.get('is_active', user.is_active)
        
        # Update user type if changed
        new_user_type = data.get('user_type')
        if new_user_type:
            if new_user_type == 'staff':
                user.is_staff = True
                user.profile.user_type = 'user'  # Reset profile type for staff
            else:
                user.is_staff = False
                user.profile.user_type = new_user_type
        
        user.save()
        user.profile.save()
        
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utente non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(is_admin)
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utente non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
