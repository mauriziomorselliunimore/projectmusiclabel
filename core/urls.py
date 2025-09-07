from django.urls import path
from .views.main import (
    home,
    populate_database,
    clear_database,
    create_superuser_render,
    render_status,
)
from .views.admin_views import (
    admin_dashboard,
    admin_artists,
    admin_associates,
    admin_bookings,
    admin_messages,
    admin_settings,
)
from .views.admin_users import (
    admin_users,
    get_user_details,
    update_user,
    toggle_user_status,
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('populate-db/', populate_database, name='populate_db'),
    path('clear-db/', clear_database, name='clear_db'),
    path('create-admin/', create_superuser_render, name='create_admin'),
    path('render-status/', render_status, name='render_status'),

    # Admin views
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/', get_user_details, name='admin_user_details'),
    path('admin/users/<int:user_id>/update/', update_user, name='admin_user_update'),
    path('admin/users/<int:user_id>/toggle-status/', toggle_user_status, name='admin_user_toggle_status'),
    path('admin/artists/', admin_artists, name='admin_artists'),
    path('admin/associates/', admin_associates, name='admin_associates'),
    path('admin/bookings/', admin_bookings, name='admin_bookings'),
    path('admin/messages/', admin_messages, name='admin_messages'),
    path('admin/settings/', admin_settings, name='admin_settings'),
]