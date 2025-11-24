from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    paginate_by = 6
    
    
    def get_queryset(self):
        # Return tasks only for the logged-in user, ordered by completion then due date
        return Task.objects.filter(owner=self.request.user).order_by('completed', 'due_date')


def task_detail(request, pk):
    # Use pk (primary key) to fetch the task
    task = get_object_or_404(Task, pk=pk)

    # Deny access if the current user is not the owner
    if task.owner != request.user:
        return HttpResponseForbidden("You do not have permission to view this task.")
    
    return render(request, "tasks/task_detail.html", {"task": task})