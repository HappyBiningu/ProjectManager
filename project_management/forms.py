from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'due_date']





# project_management/forms.py

from django import forms
from .models import Comment
from django.contrib.contenttypes.models import ContentType

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type', None)
        self.object_id = kwargs.pop('object_id', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_type = ContentType.objects.get_for_model(self.content_type)
        instance.object_id = self.object_id
        if commit:
            instance.save()
        return instance


from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']