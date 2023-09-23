from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm, CustomRegisterForm

# # Create your views here.

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
            else:
                return render(request,"registration/login_test.html",{'form':form})
                
    # 아니라면 GET요청이 온다
        else:
            form = CustomLoginForm()
    return render(request,"registration/login_test.html", {'form':form})

def register(request):

    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        # 폼 정보 확인
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('user_app:login')
    
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']

            # # 로그인 성공
            # if user is not None:
            #     # 장고 로그인 정보에 정보 저장
            #     login(request, user) 
            #     return redirect('dangun_app:main')
        else:
            return render(request,"registration/register.html",{'form':form})
            
    # 아니라면 GET요청이 온다
    else:
        form = CustomLoginForm()   
    return render(request,"registration/register.html")
