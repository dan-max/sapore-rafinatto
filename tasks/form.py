from django.forms import ModelForm
from .models  import Task, subida
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model= Task
        fields= ['title', 'description']
class UploadImg(ModelForm):
    class Meta:
        model= subida
        fields= ['image']
        