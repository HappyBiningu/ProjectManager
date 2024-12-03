from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('task/create/', views.task_create, name='task_create'),
    path('project/<int:pk>/kanban/', views.kanban_board, name='kanban_board'),
    path('task/<int:pk>/update-column/', views.update_task_column, name='update_task_column'),
    path('project/<int:pk>/gantt/', views.gantt_chart, name='gantt_chart'),
    path('upload/', views.upload_file, name='upload_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)