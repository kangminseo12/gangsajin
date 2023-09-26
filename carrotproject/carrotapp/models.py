from django.db import models
from django.contrib.auth.models import User
from user_app.models import CustomUser

# 포스트상품
class PostProduct(models.Model):
    author_id = models.CharField(max_length=32)
    buyier_id = models.CharField(max_length=32)
    category = models.CharField(max_length=64, default='선택안함')
    title = models.CharField(max_length=200)
    product = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=250)
    chat_id = models.BigIntegerField()
    view = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(null=True, upload_to='about_me/awards/%Y/%m/%d', height_field=None, width_field=None, max_length=None) # 경로 불러오는 것으로

    # 나중에 카테고리에서 외래키로 가져올 수 있도로
    # category = models.ForeignKey(
    #         'category',
    #         on_delete = models.CASCADE,
    #         )
    
class Chatting(models.Model):
    product_id = models.CharField(max_length=32)
    product_image = models.CharField(max_length=32)
    
    host_id = models.CharField(max_length=32)
    guest_id = models.CharField(max_length=32)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
