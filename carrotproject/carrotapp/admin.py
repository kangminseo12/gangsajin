from django.contrib import admin
from . import models

# Register your models here.

# 포스트를 관리자페이지와 연결
admin.site.register(models.PostProduct) 
