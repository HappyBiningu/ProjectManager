from django.db import models
from django.contrib.auth.models import User

class Requirement(models.Model):
    FUNCTIONAL = 'Functional'
    NON_FUNCTIONAL = 'Non-Functional'

    REQUIREMENT_TYPE_CHOICES = [
        (FUNCTIONAL, 'Functional'),
        (NON_FUNCTIONAL, 'Non-Functional'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    requirement_type = models.CharField(
        max_length=20,
        choices=REQUIREMENT_TYPE_CHOICES,
        default=FUNCTIONAL
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requirements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='requirements/attachments/', blank=True, null=True)
    version = models.PositiveIntegerField(default=1)  # To track the version of the requirement

    def __str__(self):
        return f"{self.title} ({self.get_requirement_type_display()})"

    class Meta:
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"







class SuccessCriteria(models.Model):
    requirement = models.ForeignKey(
        Requirement, 
        on_delete=models.CASCADE, 
        related_name="success_criteria"
    )
    description = models.TextField()
    is_met = models.BooleanField(default=False)
    test_document = models.FileField(upload_to='requirements/test_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Criteria for {self.requirement.title}: {self.description[:50]}"
