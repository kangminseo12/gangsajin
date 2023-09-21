from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'dangun_app'
urlpatterns = [
    path('', views.main,name='main'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout') # 장고 auth에서 logout 매서드 사용
]