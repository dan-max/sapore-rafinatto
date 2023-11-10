from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from .form import TaskForm, UploadImg
from .models import Task, subida
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
    images = subida.objects.all()
    print("imagenes")
    print(images)
    print("tasks")
    print(tasks)
    return render(request, 'task.html', {'tasks': tasks, 'images': images})

@login_required

def create_task(request):
    
    if request.method == 'POST':
        form = TaskForm(request.POST)  # Asegúrate de incluir request.FILES para manejar los archivos.
        images= UploadImg(request.POST, request.FILES)
        print("lee los modelos")
        if form.is_valid() and images.is_valid():
            print("los formularios son validos")
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            new_task2 = images.save(commit=False)
            new_task2.id_image = new_task
            new_task2.save()

            return redirect('task')
        else:
            print("Errores en el formulario TaskForm:", form.errors)
            print("Errores en el formulario UploadImg:", images.errors)
    else:
        form = TaskForm()
        images= UploadImg()
        print("retorna else")
    return render(request, 'create_task.html', {'form': form, 'images': images})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        images = UploadImg(request.POST, request.FILES, instance=task.subida_set.first())

        if form.is_valid() and images.is_valid():
            task = form.save(commit=False)
            task.save()

            image = images.save(commit=False)
            image.id_image = task
            image.save()

            return redirect("task")
        else:
            print("Errores en el formulario TaskForm:", form.errors)
            print("Errores en el formulario UploadImg:", images.errors)
    else:
        form = TaskForm(instance=task)
        images = UploadImg(instance=task.subida_set.first())

    return render(request, 'task_detail.html', {'task': task, 'form': form, 'images': images})

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
