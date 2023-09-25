from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.


def main(request):
    return render(request, "dangun_app/main_test.html")

# def index(request):
#     return render(request,"main.html")

def chat(request):
    return render(request, "dangun_app/chat.html")