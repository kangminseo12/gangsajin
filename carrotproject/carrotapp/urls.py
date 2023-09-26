from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import set_region, set_region_certification

from . import views


app_name = "dangun_app"
urlpatterns = [
    path("", views.main, name="main"),
    path("trade", views.trade, name="trade"),
    path("chat", views.chat, name="chat"),
    path("location", views.location, name="location"),
    path("set_region/", views.set_region, name="set_region"),
    path("set_region_certification/", set_region_certification, name="set_region_certification"),
]
