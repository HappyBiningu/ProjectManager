from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('designer', 'System Designer'),
        ('manager', 'Project Manager'),
        ('analyst', 'System Analyst'),
        ('developer', 'Developer'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname}" if self.name and self.surname else self.user.username
    
 
 
class SystemSetting(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Setting name (e.g., 'Performance')
    value = models.CharField(max_length=255)  # The value of the setting (e.g., 'Optimal')
    description = models.TextField(blank=True, null=True)  # Optional description of the setting
    is_active = models.BooleanField(default=True)  # Whether the setting is active or not

    def __str__(self):
        return self.name
    
       
    
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user.username} at {self.timestamp}"
    
    

