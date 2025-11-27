from django.urls import path
from . import views


app_name = "tasks"

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/toggle/', views.task_toggle_complete, name='task_toggle'),
]