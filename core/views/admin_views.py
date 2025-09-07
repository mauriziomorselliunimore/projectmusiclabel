from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from django.contrib.auth.models import User
from artists.models import Artist, CollaborationProposal
from associates.models import Associate, PortfolioItem
from booking.models import Booking
from messaging.models import Message, Conversation, Notification
from django.db import connection
import json
import psutil

def is_admin(user):
    """Verifica che l'utente sia staff o superadmin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def is_superadmin(user):
    """Verifica che l'utente sia un superadmin"""
    return user.is_authenticated and user.is_superuser

def get_db_stats():
    """Recupera statistiche del database"""
    with connection.cursor() as cursor:
        # Dimensione del database
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as db_size,
                   pg_size_pretty(SUM(pg_total_relation_size(c.oid))) as tables_size
            FROM pg_class c
            LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
            AND c.relkind = 'r';
        """)
        size_data = cursor.fetchone()
        
        # Numero di righe per tabella principale
        cursor.execute("""
            SELECT relname as table_name, n_live_tup as row_count
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
            LIMIT 5;
        """)
        table_stats = cursor.fetchall()
        
    return {
        'db_size': size_data[0] if size_data else 'N/A',
        'tables_size': size_data[1] if size_data else 'N/A',
        'table_stats': table_stats
    }

def get_system_metrics():
    """Recupera metriche di sistema dettagliate"""
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': {
            'per_cpu': cpu,
            'average': sum(cpu) / len(cpu),
            'cores': len(cpu)
        },
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    }

@user_passes_test(is_superadmin)
def admin_dashboard(request):
    """Dashboard principale con statistiche avanzate"""
    now = timezone.now()
    last_month = now - timedelta(days=30)
    
    # Statistiche utenti
    user_stats = {
        'total': User.objects.count(),
        'active': User.objects.filter(last_login__gte=last_month).count(),
        'new_this_month': User.objects.filter(date_joined__gte=last_month).count(),
        'artists': Artist.objects.count(),
        'associates': Associate.objects.count(),
        'user_types': User.objects.values('profile__user_type').annotate(count=Count('id'))
    }
    
    # Statistiche attività
    activity_stats = {
        'bookings': {
            'total': Booking.objects.count(),
            'pending': Booking.objects.filter(status='pending').count(),
            'confirmed': Booking.objects.filter(status='confirmed').count(),
            'completed': Booking.objects.filter(status='completed').count(),
            'cancelled': Booking.objects.filter(status='cancelled').count(),
            'revenue': Booking.objects.filter(status='completed').aggregate(Sum('total_cost'))['total_cost__sum'] or 0,
            'avg_rating': Booking.objects.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg'] or 0
        },
        'messages': {
            'total': Message.objects.count(),
            'today': Message.objects.filter(created_at__date=now.date()).count(),
            'this_week': Message.objects.filter(created_at__gte=now-timedelta(days=7)).count(),
            'active_conversations': Conversation.objects.filter(updated_at__gte=last_month).count()
        },
        'collaborations': {
            'total': CollaborationProposal.objects.count(),
            'pending': CollaborationProposal.objects.filter(status='pending').count(),
            'accepted': CollaborationProposal.objects.filter(status='accepted').count(),
            'success_rate': (CollaborationProposal.objects.filter(status='accepted').count() / 
                           max(CollaborationProposal.objects.count(), 1)) * 100
        }
    }
    
    # Metriche di sistema
    system_metrics = get_system_metrics()
    
    # Statistiche database
    db_stats = get_db_stats()
    
    # Trend di crescita
    growth_trends = {
        'users_growth': [
            User.objects.filter(date_joined__date=now.date()-timedelta(days=x)).count()
            for x in range(30, -1, -1)
        ],
        'booking_growth': [
            Booking.objects.filter(created_at__date=now.date()-timedelta(days=x)).count()
            for x in range(30, -1, -1)
        ],
        'revenue_growth': [
            Booking.objects.filter(
                created_at__date=now.date()-timedelta(days=x),
                status='completed'
            ).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
            for x in range(30, -1, -1)
        ]
    }
    
    context = {
        'active_tab': 'dashboard',
        'user_stats': user_stats,
        'activity_stats': activity_stats,
        'system_metrics': system_metrics,
        'db_stats': db_stats,
        'growth_trends': growth_trends,
        'page_title': 'Dashboard Amministrazione'
    }
    
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'active_tab': 'users',
        'users': users,
    }
    return render(request, 'admin/users.html', context)

@user_passes_test(is_admin)
def admin_artists(request):
    artists = Artist.objects.all()
    context = {
        'active_tab': 'artists',
        'artists': artists,
    }
    return render(request, 'admin/artists.html', context)

@user_passes_test(is_admin)
def admin_associates(request):
    associates = Associate.objects.all()
    context = {
        'active_tab': 'associates',
        'associates': associates,
    }
    return render(request, 'admin/associates.html', context)

@user_passes_test(is_admin)
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'bookings',
        'bookings': bookings,
    }
    return render(request, 'admin/bookings.html', context)

@user_passes_test(is_admin)
def admin_messages(request):
    messages = Message.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'messages',
        'messages': messages,
    }
    return render(request, 'admin/messages.html', context)

@user_passes_test(is_admin)
def admin_settings(request):
    context = {
        'active_tab': 'settings',
    }
    return render(request, 'admin/settings.html', context)
