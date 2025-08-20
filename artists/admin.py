from django.contrib import admin
from .models import Artist, Demo

class DemoInline(admin.TabularInline):
    model = Demo
    extra = 0

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['stage_name', 'user', 'location', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['stage_name', 'user__username', 'genres']
    inlines = [DemoInline]

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'is_public', 'uploaded_at']
    list_filter = ['genre', 'is_public', 'uploaded_at']
    search_fields = ['title', 'artist__stage_name']
