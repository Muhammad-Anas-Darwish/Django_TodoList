from django.contrib import admin
from .models import ToDoItem, ToDoList, User, Color
# Register your models here.

admin.site.register(User)
admin.site.register(ToDoList)
admin.site.register(ToDoItem)
admin.site.register(Color)