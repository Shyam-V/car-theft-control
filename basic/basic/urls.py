from django.contrib import admin
from django.urls import path

from django.urls import path
from app1 import views

urlpatterns = [
    path('',views.home),
path('login',views.login),
path('signup',views.signup),
path('mainpage',views.mainpage),
path('register',views.register),
path('dataset',views.dataset),
path('delete',views.delete),
path('control',views.control,name="control")
]
