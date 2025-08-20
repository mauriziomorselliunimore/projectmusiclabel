from django.contrib import admin
from .models import Associate, PortfolioItem

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 0

@admin.register(Associate)
class AssociateAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_level', 'hourly_rate', 'is_available', 'created_at']
    list_filter = ['experience_level', 'is_available', 'is_active', 'created_at']
    search_fields = ['user__username', 'specialization', 'skills']
    inlines = [PortfolioItemInline]

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'associate', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'associate__user__username']