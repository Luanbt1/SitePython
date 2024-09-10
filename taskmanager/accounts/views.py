from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages  # Para exibir mensagens de sucesso
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua conta foi criada com sucesso! Agora você pode fazer login.')
            return redirect('login')  # Redireciona para a página de login após o registro
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def task_list(request):
    tasks = Task.objects.all()  # Liste todas as tarefas
    return render(request, 'accounts/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'accounts/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'accounts/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'accounts/task_confirm_delete.html', {'task': task})