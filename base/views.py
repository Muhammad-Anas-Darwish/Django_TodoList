from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from datetime import datetime
from pickletools import read_stringnl_noescape
from django.http import  HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import EditItemForm, EditListForm, ProfileForm, RegisterForm
from .user_access import get_object_or_error, edit

# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if Color.objects.filter(color='black').count() == 0:
            Color.objects.create(
                color = "black"
            )

        id_color = Color.objects.get(color='black')

        ToDoList.objects.create(
            user = request.user,
            todo_list = request.POST.get('title'),
            color = id_color
        )

    todo_list = ToDoList.objects.filter(user=request.user)

    context = {
        'lists': todo_list,
    }
    return render(request,  'base/home.html', context)

@login_required(login_url='login')
def todo_list(request, pk):
    todo_list = ToDoList.objects.get(id=pk)

    if request.method == 'POST':
        ToDoItem.objects.create(
            user = request.user,
            todo_list = todo_list,
            title = request.POST.get('title'),
            description = '',
            date_created = datetime.now()
        )

    if request.user == todo_list.user:
        items = ToDoItem.objects.filter(todo_list = todo_list)
    else:
        return HttpResponse("ERROR 404!!")

    context = {
        'list': todo_list,
        'items': items,
    }
    return render(request, 'base/list.html', context)

@login_required(login_url='login')
def delete_list(request, pk):
    todo_list = get_object_or_error(ToDoList, pk)

    if request.method == 'POST':
        if todo_list.user == request.user:
            todo_list.delete()
            return redirect(home)
        else:
            return HttpResponse("ERROR 404!!")
    return render(request, 'base/delete_list.html', {'list':todo_list})

@login_required(login_url='login')
def delete_item(request, pk):
    todo_item = get_object_or_error(ToDoItem, pk)
        
    if todo_item.user == request.user:
        ToDoItem.objects.get(id=pk).delete()
        return redirect('todo_list', pk=todo_item.todo_list.id)
    else:
        return HttpResponse("ERROR 404!!")

def edit_list(request, pk):
    return edit(request, pk, ToDoList, 'home', 'base/edit_list.html', EditListForm)

def edit_item(request, pk):
    return edit(request, pk, ToDoItem, 'todo_list', 'base/edit_item.html', EditItemForm)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User OR password does not exit")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.save()
            login(request, form)
            return redirect('home')

    context = {
        'page': page,
        'form': form,
        }
    return render(request, 'base/login_register.html', context)

login_required(login_url='login')
def profile(request):
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/profile.html', {'form': form})
