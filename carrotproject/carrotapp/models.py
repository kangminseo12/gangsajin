from django.db import models


# 포스트상품
class PostProduct(models.Model):
    author_id = models.CharField(max_length=30)
    buyier_id = models.CharField(max_length=30)
    category = models.CharField(max_length=50, default='선택안함')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=250)
    chat_id = models.BigIntegerField()
    view = models.IntegerField(default=0)
    state = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.CharField() # 경로 불러오는 것으로

# class Chatting(models.Model):
#     product_id = models.CharField()
#     product_image = models.CharField()
    
    # 신청자_id = models.CharField()
    # 답변자_id = models.CharField()