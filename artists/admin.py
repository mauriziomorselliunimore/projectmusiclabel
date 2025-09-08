from django.contrib import admin
from .models import Artist, Demo

class DemoInline(admin.TabularInline):
    model = Demo
    extra = 0


@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'is_public', 'uploaded_at']
    list_filter = ['genre', 'is_public', 'uploaded_at']
    search_fields = ['title', 'artist__stage_name']
