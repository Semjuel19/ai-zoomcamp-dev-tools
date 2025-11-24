from django.contrib import admin
from .models import TODO


@admin.register(TODO)
class TODOAdmin(admin.ModelAdmin):
    """Admin interface for TODO model"""
    list_display = ['title', 'due_date', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'
    list_editable = ['is_resolved']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Status & Dates', {
            'fields': ('is_resolved', 'due_date')
        }),
    )
