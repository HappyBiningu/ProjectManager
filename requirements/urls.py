from django.urls import path
from . import views

urlpatterns = [
    path('', views.requirement_list, name='requirement_list'),  
    path('create/', views.requirement_create, name='requirement_create'),
    path('update/<int:id>/', views.requirement_update, name='requirement_update'),
    path('<int:pk>/delete/', views.requirement_delete, name='requirement_delete'),
    path('success_criteria/', views.success_criteria_list, name='success_criteria_list'),
    path('success_criteria/create/', views.success_criteria_create, name='success_criteria_create'),
    path('success_criteria/<int:pk>/update/', views.success_criteria_update, name='success_criteria_update'),
]
