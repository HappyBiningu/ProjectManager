from django.db import models
from requirements.models import Requirement

class UseCase(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    actors = models.TextField(help_text="List the actors involved in the use case.")
    preconditions = models.TextField(help_text="Conditions that must be met before the use case begins.")
    steps = models.TextField(help_text="Detailed steps of the use case.")
    postconditions = models.TextField(help_text="Expected results after the use case is completed.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='use_cases')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

