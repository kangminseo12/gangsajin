from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dangun_app'
urlpatterns = [
    path('', views.main,name='main'),
]