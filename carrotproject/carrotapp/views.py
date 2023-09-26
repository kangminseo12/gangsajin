from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import PostProduct, ChatRoom, Message
from user_app.models import CustomUser

# Create your views here.
def main(request):
    return render(request, "dangun_app/main_test.html")

@login_required
def chatroom_list(request):
    # 채팅방 리스트 중 하나를 클릭했을 경우
    # if request.method == "POST":
    #     chatroom_id = request.

    
    # chat 화면을 처음 들어왔을 경우 채팅방 리스트를 뿌려줌
    user = request.user

    # 현재 로그인한 사용자가 chat_host 또는 chat_guest인 ChatRoom을 검색
    chatrooms = ChatRoom.objects.filter(
        Q(chat_host=user.id) | Q(chat_guest=user.id)
    )

    # 최종적으로 넘겨줄 결과 chatroom 리스트 초기화
    context = []

    # 각 chatroom에 대해 필요한 정보 가져옴
    for chatroom in chatrooms:
        
        # 채팅 상대 정보
        if chatroom.chat_host == user.id:
            chat_partner = CustomUser.objects.get(id=chatroom.chat_host)
        else:
            chat_partner = CustomUser.objects.get(id=chatroom.chat_guest)
        
        # 상품
        product = PostProduct.objects.get(id=chatroom.product_id)
        
        # 마지막 주고 받은 메시지
        last_message = Message.objects.filter(chatroom_id=chatroom.id).order_by('-sent_at').first()

        result = {
            
            'chat_partner' : chat_partner, # 채팅 상대방의 정보
            'product' : product, # 상품 정보
            'message' : last_message # 마지막 메시지 정보
        }

        context.append(result)

    return render(request, 'dangun_app/chat.html', {'context' : context})

@login_required
def chatroom(request, chatroom_id):
    # 현재 로그인한 사용자의 정보
    user = request.user
    
    # 채팅 상대 정보
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    
    if chatroom.chat_host == user.id:
        chat_partner = CustomUser.objects.get(id=chatroom.chat_host)
    else:
        chat_partner = CustomUser.objects.get(id=chatroom.chat_guest)

    return render(request, "dangun_app/chat.html", {"chatroom_id" : chatroom_id})