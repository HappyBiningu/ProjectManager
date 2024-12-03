from django.contrib import admin
from .models import Project, Task, Comment, File

# Admin for Project model
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin.site.register(Project, ProjectAdmin)

# Admin for Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'column', 'due_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'assigned_to__username')
    list_filter = ('status', 'column', 'assigned_to')
    ordering = ('-created_at',)
    date_hierarchy = 'due_date'

admin.site.register(Task, TaskAdmin)

# Admin for Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at', 'updated_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Comment, CommentAdmin)

# Admin for File model
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'uploaded_by', 'uploaded_at')
    search_fields = ('name', 'project__title', 'uploaded_by__username')
    list_filter = ('project', 'uploaded_by')
    ordering = ('-uploaded_at',)
    date_hierarchy = 'uploaded_at'

admin.site.register(File, FileAdmin)
