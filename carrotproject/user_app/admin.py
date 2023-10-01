from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# 다국어 지원기능
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


# Register your models here.
# 커스텀유저을 추가
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "nickname", "email")


class MyUserAdmin(UserAdmin):
    # 수정누를때 나오는창
    fieldsets = (
        (
            "필수정보",
            {
                "fields": (
                    "username",
                    "nickname",
                    "email",
                    "password",
                )
            },
        ),
        ("상제정보", {"fields": ("date_joined", "location", "location_v", "manner")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )
    # 추가할때 나오는 창
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "nickname",
                    "email",
                    "password1",
                    "password2",
                    "date_joined",
                    "location",
                    "manner",
                ),
            },
        ),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ("id", "username", "nickname", "email", "is_staff")
    list_filter = ("id", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("id", "username", "nickname", "email")


admin.site.register(CustomUser, MyUserAdmin)
