from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Location

from django.http import JsonResponse
from django.contrib import messages

from user_app.models import CustomUser
from django.utils.translation import gettext_lazy as _

# Create your views here.


def main(request):
    return render(request, "dangun_app/main.html")


def trade(request):
    return render(request, "dangun_app/trade.html")


def chat(request):
    return render(request, "dangun_app/chat.html")


# 동네인증 화면 갈때
@login_required
def location(request):
    region = request.user.location

    return render(request, "dangun_app/location.html", {"region": region})


# 지역설정
@login_required
def set_region(request):
    if request.method == "POST":
        region = request.POST.get("region-setting")

        if region:
            try:
                user_profile = request.user
                user_profile.location = region
                user_profile.save()

                return redirect("dangun_app:location")
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "Region cannot be empty"})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        custom_user = request.user
        # custom_user.location = "Y"

        custom_user.save()

        messages.success(request, _("인증되었습니다"))

        return redirect("dangun_app:main")
