from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from .form import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def helloworld(request):
    return render(request, 'home.html', {
        
    })

def singup(request):
    if request.method== 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(username=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("task")
            except:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'username already exist'
                })
        return render(request, 'singup.html',{
            'form': UserCreationForm,
            'error': 'password do not match'
        })

@login_required

def singout(request):
    logout(request)
    return redirect('home')

def singin(request):

    if request.method == "GET":

        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user=authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('task')

@login_required

def tasks (request):
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'task.html', {'tasks': tasks})

@login_required

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar los archivos.
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task")
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_detail.html', {'task': task, 'form': form})

@login_required

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect ('task')

@login_required

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.delete()
        return redirect ('task')

@login_required
def task_completed(request):
    tasks= Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render (request, 'task.html', {'tasks': tasks})
