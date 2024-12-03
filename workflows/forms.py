from django import forms
from .models import Workflow

class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ['name', 'description', 'use_case', 'diagram_data']
        widgets = {
            'diagram_data': forms.HiddenInput(),
        }
