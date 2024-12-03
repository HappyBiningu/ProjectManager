# users/middleware.py

from django.http import HttpResponseForbidden

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted URLs and required roles
        role_restricted_views = {
            '/dashboard/designer/': 'designer',
            '/dashboard/manager/': 'manager',
            '/dashboard/analyst/': 'analyst',
            '/dashboard/developer/': 'developer',
            '/dashboard/admin/': 'admin',
        }
        required_role = role_restricted_views.get(request.path)
        if required_role and request.user.is_authenticated:
            if request.user.profile.role != required_role:
                return HttpResponseForbidden("You don't have access to this page.")
        return self.get_response(request)
