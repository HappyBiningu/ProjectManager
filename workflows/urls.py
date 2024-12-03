from django.urls import path
from . import views

urlpatterns = [
    path('', views.workflow_list, name='workflow_list'),
    path('create/', views.workflow_create, name='workflow_create'),
    path('<int:pk>/update/', views.workflow_update, name='workflow_update'),
    path('<int:pk>/delete/', views.workflow_delete, name='workflow_delete'),
]
