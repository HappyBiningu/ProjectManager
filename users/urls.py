from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    designer_dashboard,
    manager_dashboard,
    analyst_dashboard,
    developer_dashboard,
    admin_dashboard,
)

urlpatterns = [
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register_user, name='register'),

    # Home URL
    path('', views.home, name='home'),

    # Dashboard URLs
    path('dashboard/designer/', designer_dashboard, name='designer_dashboard'),
    path('dashboard/manager/', manager_dashboard, name='manager_dashboard'),
    path('dashboard/analyst/', analyst_dashboard, name='analyst_dashboard'),
    path('dashboard/developer/', developer_dashboard, name='developer_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    
    #admin urls
    path('user-management/', views.user_management, name='user_management'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('settings/update/<int:setting_id>/', views.update_settings, name='update_settings'),
]
