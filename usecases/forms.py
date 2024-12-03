from django import forms
from .models import UseCase

class UseCaseForm(forms.ModelForm):
    class Meta:
        model = UseCase
        fields = ['title', 'actors', 'preconditions', 'steps', 'postconditions', 'status', 'requirement']
