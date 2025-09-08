from django.contrib import admin
from .models import Associate, PortfolioItem

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 0


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'associate', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'associate__user__username']