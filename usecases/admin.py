from django.contrib import admin
from .models import UseCase

# Admin for UseCase model
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'requirement', 'created_at', 'updated_at')
    search_fields = ('title', 'actors', 'preconditions', 'steps', 'postconditions', 'requirement__title')
    list_filter = ('status', 'requirement')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')  # Mark non-editable fields as read-only

    fieldsets = (
        (None, {
            'fields': ('title', 'actors', 'preconditions', 'steps', 'postconditions', 'status', 'requirement')
        }),
        ('Date Information', {
            'fields': ('updated_at',),  # Include only editable or read-only fields
            'classes': ('collapse',)
        }),
    )

admin.site.register(UseCase, UseCaseAdmin)
