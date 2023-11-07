"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
#aqui almacenamos nuestras vistas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.helloworld, name='home'),
    path('singup/', views.singup, name='singup'),
    path('task/', views.tasks, name='task'),
    path('task/create/', views.create_task, name='create_task'),
    path('logout/', views.singout, name='singout'),
    path('singin/', views.singin, name='singin'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('task_completed/', views.task_completed, name='task_completed'),
]
'''
solo en desarrollo, en produccion hay que agregar un engine
'''
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    
