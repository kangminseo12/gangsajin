from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import CustomLoginForm

# Create your views here.


def main(request):
    return render(request, "dangun_app/main_test.html")

# def index(request):
#     return render(request,"main.html")

def custom_login(request):
    # 로그인이 된경우
    # 관리자계정확인
    if request.user.is_authenticated:
        return redirect('dangun_app:main')

    # 로그인이 안된경우
    else :
        form = CustomLoginForm(data=request.POST or None)
        if request.method == "POST":

            # 폼 정보 확인
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # 슈퍼유저인지 확인
                user = authenticate(request, username=username, password=password)

                # 로그인 성공
                if user is not None:
                    # 장고 로그인 정보에 정보 저장
                    login(request, user) 
                    return redirect('dangun_app:main')
    # 아니라면 GET요청이 온다
    return render(request,"registration/login_test.html", {'form':form})

# def register(request):
#     return render(request,"register.html")
