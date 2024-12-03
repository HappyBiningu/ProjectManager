from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', next_page='/dashboard/'), name='login'),
    path('users/', include('users.urls')),
    path('requirements/', include('requirements.urls')),
    path('usecases/', include('usecases.urls')),
    path('workflows/', include('workflows.urls')),
    path('', views.home, name='home'), 

    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



