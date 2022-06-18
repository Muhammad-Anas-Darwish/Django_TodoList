from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import ToDoItem, ToDoList, User

class EditListForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['todo_list', 'color']

class EditItemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['description']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar']