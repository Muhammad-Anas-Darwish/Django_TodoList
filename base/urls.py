from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views #import this


urlpatterns = [
    path('', home, name="home"),
    path('list/<int:pk>/', todo_list, name="todo_list"),

    path('list/delete/<int:pk>', delete_list, name='delete_list'),
    path('item/delete/<int:pk>', delete_item, name='delete_item'),

    path('list/edit/<int:pk>', edit_list, name='edit_list'),
    path('item/edit/<int:pk>', edit_item, name='edit_item'),

    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('signup/', registerPage, name="register"),

    path('profile/', profile, name='profile'),
]