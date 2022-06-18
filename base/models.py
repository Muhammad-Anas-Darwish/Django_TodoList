from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_list = models.CharField(max_length=200)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.todo_list

class ToDoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title