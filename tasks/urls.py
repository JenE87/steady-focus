from django.urls import path
from . import views


app_name = "tasks"

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>', views.task_detail, name='task_detail'),
]