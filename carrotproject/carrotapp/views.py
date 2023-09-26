from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import PostProduct

# Create your views here.


def main(request):
    return render(request, "dangun_app/main_test.html")

# def index(request):
#     return render(request,"main.html")

def trade(request):
    top_views_posts = PostProduct.objects.all()
    return render(request, 'dangun_app/trade.html', {'posts': top_views_posts})