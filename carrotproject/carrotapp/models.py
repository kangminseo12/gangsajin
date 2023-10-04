from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from user_app.models import CustomUser
from mptt.models import MPTTModel, TreeForeignKey



# 계층 트리 구조 카테고리 추가 MPTTModel 이용
class Category(MPTTModel):
    name = models.CharField(verbose_name="카테고리 명", max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name="상위 카테고리", on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
    

# 포스트상품
class PostProduct(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    buyier_id = models.CharField(max_length=32, blank=True)
    category = TreeForeignKey(Category, verbose_name="카테고리", on_delete=models.CASCADE, db_index=True,default=1 )
    title = models.CharField(max_length=200)
    # 물품정보는 현재 사용하지 않고 타이틀만 사용
    product = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=250, default="지정안함")
    chat_id = models.BigIntegerField(default=0)
    view = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default="N")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        null=True,
        upload_to="img/%Y/%m/%d",
        height_field=None,
        width_field=None,
        max_length=None,
    )  

class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(PostProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chat_host = models.IntegerField()
    chat_guest = models.IntegerField()


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    sender = models.IntegerField()
    receiver = models.IntegerField()
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Comment(models.Model):
    post = models.ForeignKey(PostProduct, on_delete=models.CASCADE)
    author = models.CharField(max_length=255, default="User")  # 기본값을 "User"로 설정
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
