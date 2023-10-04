from django.contrib import admin
from . import models
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
class PostProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'buyier_id', 'category','location','status')
    list_display_links = ('id', 'title', 'author', 'buyier_id', 'category','location','status')
    list_filter = ('id','title','author',  'buyier_id','category','status' )
    search_fields = ( 'id','title', 'author', 'buyier_id','category','status' )

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_host', 'chat_guest', 'product', 'created_at')
    list_display_links = ('id', 'chat_host', 'chat_guest', 'product', 'created_at')
    list_filter = ('id','chat_host','chat_guest',  'product' )
    search_fields = ( 'id','product', 'chat_host', 'chat_guest')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver','is_read')
    list_display_links = ('id', 'sender', 'receiver','is_read')
    list_filter = ('id','sender','receiver', 'is_read')

    search_fields = ( 'id','sender', 'receiver')


# 드래그를 지원하는 클래스모델
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'name',
    )
    mptt_level_indent = 20



# 포스트를 관리자페이지와 연결
admin.site.register(models.PostProduct,PostProductAdmin) 
admin.site.register(models.ChatRoom,ChatRoomAdmin)
admin.site.register(models.Message,MessageAdmin)
admin.site.register(models.Category, CategoryAdmin)
