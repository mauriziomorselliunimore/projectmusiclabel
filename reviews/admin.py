from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewed', 'review_type', 'rating', 'title', 'created_at']
    list_filter = ['review_type', 'created_at']
    search_fields = ['reviewer__username', 'reviewed__username', 'title', 'content']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reviewer', 'reviewed')
        
    def has_module_permission(self, request):
        # Permetti l'accesso al modulo solo agli admin
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        # Permetti la visualizzazione a tutti gli admin
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        # Permetti la modifica solo ai superuser
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Permetti l'eliminazione solo ai superuser
        return request.user.is_superuser
"""
All review admin registrations have been removed as reviews are no longer needed.
"""
