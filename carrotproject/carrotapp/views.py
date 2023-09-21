from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,"registration/login_test.html")

# def register(request):
#     return render(request,"register.html")

# def index(request):
#     return render(request,"main.html")