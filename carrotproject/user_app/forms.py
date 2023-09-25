from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        error_messages={"required" : "아이디를 입력해주세요"},
        label='',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요', 'class': 'login-input'}),
        error_messages={"required" : "비밀번호를 입력해주세요."},
        label='',
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if password and username :
            try:
                user = CustomUser.objects.get(username = username)
            except CustomUser.DoesNotExist:
                self.add_error("username", "아이디가 존재하지 않습니다.")
                return 

            if not check_password(password, user.password):
                self.add_error("username", "비밀번호가 일치하지 않습니다.")
                return 
            else:
                self.user_id = user.id
                
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = CustomUser
        exclude = ['created_at']
        fields = ('username', 'password1','password2','email','nickname')
