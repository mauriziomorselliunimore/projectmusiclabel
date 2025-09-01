from django.urls import path
from .views.main import (
    home,
    populate_database,
    clear_database,
    create_superuser_render,
    render_status,
)

from .views.admin import control_panel

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('populate-db/', populate_database, name='populate_db'),
    path('clear-db/', clear_database, name='clear_db'),
    path('create-admin/', create_superuser_render, name='create_admin'),
    path('render-status/', render_status, name='render_status'),

    
    # Admin views
    path('admin/control-panel/', control_panel, name='admin_control_panel'),
]