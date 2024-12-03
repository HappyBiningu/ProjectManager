from django import forms
from .models import Requirement

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = [
            'title', 
            'description', 
            'requirement_type',   # Added new field
            'priority', 
            'status', 
            'attachment',        # Changed to match the model (file field renamed)
        ]



from .models import SuccessCriteria

class SuccessCriteriaForm(forms.ModelForm):
    class Meta:
        model = SuccessCriteria
        fields = ['requirement', 'description', 'is_met', 'test_document']
