from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'user_app'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout') # 장고 auth에서 logout 매서드 사용
]
