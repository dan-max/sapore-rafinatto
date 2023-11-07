from time import timezone
from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField(blank=True)
    created= models.DateTimeField(auto_now_add=True)
    datecompleted= models.DateTimeField(null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='upload', null=True)
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username