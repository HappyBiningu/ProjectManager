from django.db import models
from usecases.models import UseCase

class Workflow(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE, related_name='workflows')
    diagram_data = models.JSONField(help_text="Stores JSON representation of the diagram.", blank=True, null=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
