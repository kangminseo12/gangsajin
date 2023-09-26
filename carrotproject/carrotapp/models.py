from django.db import models

from django.conf import settings
from django.contrib.auth.models import User


# 포스트상품
class PostProduct(models.Model):
    author_id = models.CharField(max_length=32)
    buyier_id = models.CharField(max_length=32)
    category = models.CharField(max_length=64, default="선택안함")
    title = models.CharField(max_length=200)
    product = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=250)
    chat_id = models.BigIntegerField()
    view = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default="N")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.CharField(max_length=1500)  # 경로 불러오는 것으로

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


# 지워도 문제없을듯합니다..?
class Location(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="locations"
    )
    location_type = models.CharField(max_length=10)
    location_1 = models.CharField(max_length=(1500))
    location_2 = models.CharField(max_length=(1500))

    class Meta:
        unique_together = ("user", "location_type")


# 사용자가 지역을 2개 가지고 싶다는것에 대한 gpt 답변..
# 이렇게 하면 User 객체에서 .locations.filter(location_type='primary')
# 와 같은 방식으로 주요 위치나 보조 위치에 접근할 수 있습니다.
# 위 코드에서 unique_together 옵션은 같은 사용자가
# 동일한 location_type을 가진 여러 Location 객체를 가지지 못하도록 합니다.
