from django.urls import path
from . import views

urlpatterns = [
    path('', views.usecase_list, name='usecase_list'),
    path('create/', views.usecase_create, name='usecase_create'),
    path('<int:pk>/update/', views.usecase_update, name='usecase_update'),
    path('<int:pk>/delete/', views.usecase_delete, name='usecase_delete'),
]
