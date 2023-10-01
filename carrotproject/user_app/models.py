from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


"""
장고에서 기본제공하는 admin에는 아이디,비번,이메일로 필드가 정해져 있다.
추가적인 필드 정보를 위해 위해 커스텀 유저폼을 만든다.
https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model

커스텀 유저모델을 만드는 3가지 방법
- 표준 User 모델과 1대 1 관계를 가지는 모델을 만드는 방법
- AbstractUser을 상속받는 모델을 만드는 방법
- (사용)AbstractBaseUser을 상속받는 모델을 만드는 방법
"""


# AbstracBaseUser 장고 기본 유저모델을 상속받음
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, nickname, email, password, **extra_fields):
        username = self.model.normalize_username(username)
        if not nickname:
            raise ValueError("닉네임을 입력해주세요")
        nickname = self.model.normalize_username(nickname)
        if not email:
            raise ValueError("이메일을 입력해주세요")
        email = self.normalize_email(email)
        print("입력된 유저네임:")
        print(username)
        print("-------확인선-------")

        user = self.model(username=username, nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, nickname, email, password, **extra_fields)

    def create_superuser(self, username, nickname, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff=True일 필요가 있습니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser=True일 필요가 있습니다.")
        return self._create_user(username, nickname, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("사용자이름"), max_length=20, unique=True)
    email = models.EmailField(_("이메일주소"), unique=True, null=True)
    nickname = models.CharField(_("닉네임"), max_length=20, unique=True)
    date_joined = models.DateTimeField(_("생성일"), default=timezone.now)
    location = models.CharField(("지역"), max_length=100, default="인증필요")
    location_v = models.CharField(("지역인증"), max_length=1, default="N")
    manner = models.IntegerField(
        ("온도"), validators=[MinValueValidator(0), MaxValueValidator(100)], default=50
    )

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    objects = UserManager()
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
