from django.contrib import admin
from .models import Requirement, SuccessCriteria

# Admin for Requirement model
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('title', 'requirement_type', 'priority', 'status', 'created_by', 'created_at', 'updated_at', 'version')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('requirement_type', 'priority', 'status', 'created_by')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'requirement_type', 'priority', 'status', 'created_by', 'attachment', 'version')
        }),
        ('Date Information', {
            'fields': ('updated_at',),  # Only include editable fields
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only in the admin

admin.site.register(Requirement, RequirementAdmin)

# Admin for SuccessCriteria model
class SuccessCriteriaAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'description', 'is_met', 'created_at', 'updated_at')
    search_fields = ('description', 'requirement__title')
    list_filter = ('is_met',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin.site.register(SuccessCriteria, SuccessCriteriaAdmin)
