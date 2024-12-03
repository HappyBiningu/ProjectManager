from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm
from requirements.models import Requirement
from project_management.models import Project
from usecases.models import UseCase
from project_management.models import Task
from users.models import User,Profile, SystemSetting, AuditLog 
from workflows.models import Workflow
from django.db.models import Count, F
import psutil
import logging
from django.utils import timezone

# User Registration View
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Update with the login URL name
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# Custom Login View
class CustomLoginView(LoginView):
    def get_success_url(self):
        user_profile = self.request.user.profile
        role_to_dashboard = {
            'designer': 'designer_dashboard',
            'manager': 'manager_dashboard',
            'analyst': 'analyst_dashboard',
            'developer': 'developer_dashboard',
            'admin': 'admin_dashboard',
        }
        return reverse(role_to_dashboard.get(user_profile.role, 'home'))


# Home View
def home(request):
    return render(request, 'registration/home.html')


# Role-Specific Dashboards
@login_required
def designer_dashboard(request):
    # Check if the user is a designer
    if request.user.profile.role != 'designer':
        return HttpResponseForbidden("You don't have access to this page.")
    
    # Get the count of projects
    total_projects = Project.objects.count()

    # Get the count of completed tasks
    completed_tasks = Task.objects.filter(status='completed').count()

    # Get the count of pending requirements
    pending_requirements = Requirement.objects.filter(status='pending').count()

    # Get the count of use cases with different statuses
    use_cases_draft = UseCase.objects.filter(status='draft').count()
    use_cases_under_review = UseCase.objects.filter(status='under_review').count()
    use_cases_approved = UseCase.objects.filter(status='approved').count()

    # Get the total number of workflows
    total_workflows = Workflow.objects.count()

    # Fetch profile data
    profile = request.user.profile

    # Get the count of tasks assigned to the logged-in user
    assigned_tasks = Task.objects.filter(assigned_to=request.user).count()

    # Prepare the context for the template
    context = {
        'total_projects': total_projects,
        'completed_tasks': completed_tasks,
        'pending_requirements': pending_requirements,
        'use_cases_draft': use_cases_draft,
        'use_cases_under_review': use_cases_under_review,
        'use_cases_approved': use_cases_approved,
        'total_workflows': total_workflows,
        'profile': profile,
        'assigned_tasks': assigned_tasks,
    }

    return render(request, 'dashboards/designer_dashboard.html', context)




@login_required
def manager_dashboard(request):
    if request.user.profile.role != 'manager':
        return HttpResponseForbidden("You don't have access to this page.")
    
    context = {
        'profile': request.user.profile, 
    }
    return render(request, 'dashboards/manager_dashboard.html', context)


@login_required
def analyst_dashboard(request):
    if request.user.profile.role != 'analyst':
        return HttpResponseForbidden("You don't have access to this page.")
    
    context = {
        'profile': request.user.profile, 
    }
    return render(request, 'dashboards/analyst_dashboard.html', context)


@login_required
def developer_dashboard(request):
    if request.user.profile.role != 'developer':
        return HttpResponseForbidden("You don't have access to this page.")
    
    context = {
        'profile': request.user.profile, 
    }
    return render(request, 'dashboards/developer_dashboard.html', context)


@login_required
def admin_dashboard(request):
    # Only allow access to users with 'admin' role
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("You don't have access to this page.")
    
    # Retrieve dynamic data for the dashboard
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    delayed_projects = Project.objects.filter(status='delayed').count()

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    not_started_tasks = Task.objects.filter(status='not_started').count()

    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    # Get pending registrations: Users who don't have a name or surname
    pending_users = User.objects.filter(profile__name__isnull=True, profile__surname__isnull=True).count()

    # Get suspended accounts: Assuming there's an is_suspended field in Profile model
    suspended_accounts = User.objects.filter(profile__is_suspended=True).count()  # Modify based on your model

    total_requirements = Requirement.objects.count()

    workflows = Workflow.objects.all()
    use_cases = UseCase.objects.all()
    
    
     # System Health Data (Actual Logic)
    system_performance = "Optimal"
    try:
        # CPU Usage Percentage
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 85:
            system_performance = "High CPU Usage"
        elif cpu_usage > 60:
            system_performance = "Moderate CPU Usage"
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        if memory_usage > 85:
            system_performance = "High Memory Usage"
        elif memory_usage > 60:
            system_performance = "Moderate Memory Usage"
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        if disk_usage > 85:
            system_performance = "High Disk Usage"
        elif disk_usage > 60:
            system_performance = "Moderate Disk Usage"
    except Exception as e:
        system_performance = f"Error in fetching performance: {str(e)}"

    # Resource Usage (CPU, Memory, Disk)
    resource_usage = {
        'CPU': psutil.cpu_percent(interval=1),
        'Memory': psutil.virtual_memory().percent,
        'Disk': psutil.disk_usage('/').percent,
    }

    # System Notifications
    system_notifications = []
    # Check for critical system notifications, e.g., disk space running low or errors
    if psutil.disk_usage('/').percent > 85:
        system_notifications.append("Disk space is running low.")
    if psutil.virtual_memory().percent > 85:
        system_notifications.append("Memory usage is critically high.")
    if psutil.cpu_percent(interval=1) > 85:
        system_notifications.append("CPU usage is too high.")

    # Pass data to the template
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'delayed_projects': delayed_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'not_started_tasks': not_started_tasks,
        'total_users': total_users,
        'active_users': active_users,
        'pending_users': pending_users,
        'suspended_accounts': suspended_accounts,
        'total_requirements': total_requirements,
        'workflows': workflows,
        'use_cases': use_cases,
        'profile': request.user.profile, 
        'system_performance': system_performance,
        'resource_usage': resource_usage,
        'system_notifications': system_notifications,
    }
    
    return render(request, 'dashboards/admin_dashboard.html', context)





@login_required
def user_management(request):
    # Only allow access to users with 'admin' role
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("You don't have access to this page.")
    
    users = User.objects.all()  # Get all users
    profiles = Profile.objects.all()  # Get all profiles

    context = {
        'users': users,
        'profiles': profiles,
    }

    return render(request, 'admin/user_management.html', context)

@login_required
def edit_user(request, user_id):
    # Only allow access to users with 'admin' role
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("You don't have access to this page.")
    
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        # Update user fields
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_active = 'is_active' in request.POST
        user.save()

        # Update profile fields
        profile.role = request.POST['role']
        profile.is_suspended = 'is_suspended' in request.POST
        profile.save()

        return redirect('user_management')  # Redirect back to user management page

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'admin/edit_user.html', context)



# Set up a logger for audit trail
logger = logging.getLogger(__name__)

@login_required
def admin_settings(request):
    # Only allow access to users with 'admin' role
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("You don't have access to this page.")
    
    # Retrieve system settings from the database (modify with your actual settings)
    system_settings = SystemSetting.objects.all()

    # Retrieve audit log
    audit_logs = AuditLog.objects.all().order_by('-timestamp')[:10]  # Get the last 10 audit logs

    context = {
        'system_settings': system_settings,
        'audit_logs': audit_logs,
        'profile': request.user.profile,  # Include profile for header info
    }

    return render(request, 'admin/admin_settings.html', context)

# View to update settings
@login_required
def update_settings(request, setting_id):
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("You don't have access to this page.")
    
    setting = SystemSetting.objects.get(id=setting_id)

    if request.method == "POST":
        # Update the setting value
        new_value = request.POST.get('value')
        setting.value = new_value
        setting.save()

        # Create an audit log entry
        AuditLog.objects.create(
            action="Updated setting",
            description=f"Updated setting {setting.name} to {new_value}",
            user=request.user,
            timestamp=timezone.now()
        )

        # Redirect back to the settings page
        return redirect('settings')  # Make sure 'settings' is the correct URL name

    # If it's a GET request, render the individual setting page
    context = {
        'setting': setting
    }
    return render(request, 'admin/setting.html', context)