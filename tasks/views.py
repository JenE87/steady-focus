from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from .forms import TaskForm
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


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('tasks:task_list')
        
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    """
    POST > validate and save (owner remains)
    GET > show task form with instance populated (owner must match)
    """
    task = get_object_or_404(Task, pk=pk)

    if task.owners != request.user:
        return HttpResponseForbidden("You do not have permission to edit this task.")
        
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('tasks:task_detail', pk=task.pk)
        else:
            messages.error(request, "Task not updated. Please correct the errors below.")
    else:
        form = TaskForm(instance=task)
        
    return render(request, 'tasks/task_form', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    """
    POST > delete and redirect
    GET > show confirmation page
    """
    task = get_object_or_404(Task, pk)

    if task.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this task.")
    
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('task:task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})