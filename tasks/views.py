import json # For handling JSON responses
from django.http import JsonResponse, HttpResponse # For returning JSON/HTTP responses
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Decorator to enforce login
from django.contrib.auth.forms import UserCreationForm # For user registration
from django.contrib import messages # To display success/error messages
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # Use our custom RegistrationForm
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password) # type: ignore # Create user
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to login page after successful registration
        else:
            # If form is invalid, messages.error will show errors for fields
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required # Ensures only logged-in users can access this view
def task_list(request):
    # Fetch tasks only for the currently logged-in user
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm() # Initialize an empty form for adding new tasks

    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) # Don't save yet, we need to assign the user
            task.user = request.user      # Assign the current logged-in user to the task
            task.save()                   # Now save the task to the database
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')  # Redirect back to the task list
        else:
            messages.error(request, 'Error adding task. Please check the form.')
            # If the form is invalid, we might want to re-render task_list with errors
            # For now, a simple redirect or pass errors to template (more advanced)
            tasks = Task.objects.filter(user=request.user) # Fetch tasks again
            return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
    else:
        # If accessed via GET, redirect to task_list or render a blank form (not typical for add_task)
        return redirect('task_list') # Typically, add is part of the list page
    
@login_required
@require_POST # Ensure this view only accepts POST requests
def toggle_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user) # Ensure user owns task
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found or unauthorized'}, status=404)

    task.completed = not task.completed # Toggle the completed status
    task.save()
    return JsonResponse({'success': True, 'completed': task.completed})

@login_required
@require_POST # Ensure this view only accepts POST requests
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user) # Ensure user owns task
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found or unauthorized'}, status=404)

    task.delete()
    messages.success(request, 'Task deleted successfully!') # Messages work fine with redirects, but not directly with AJAX for displaying on the same page without reload
    return JsonResponse({'success': True})