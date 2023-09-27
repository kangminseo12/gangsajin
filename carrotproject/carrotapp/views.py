from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from django.contrib import messages

from django.db.models import Q
from .models import PostProduct, ChatRoom, Message

from user_app.models import CustomUser
from django.utils.translation import gettext_lazy as _
from .forms import PostForm

# 포스팅
import uuid


# Create your views here.

def main(request):
    list_post = PostProduct.objects.filter(status="N").order_by('-view')
    return render(request, "dangun_app/main.html", {'posts': list_post})


def trade(request):
    top_views_posts = PostProduct.objects.filter(status="N").order_by('-view')
    return render(request, 'dangun_app/trade.html', {'posts': top_views_posts})

def search(request):
    search_data = request.GET.get("search")
    search_list = PostProduct.objects.filter(Q(title__icontains=search_data)|Q(location__icontains=search_data)) 
    return render(request, "dangun_app/search.html", {'posts': search_list})


@login_required
def write(request, post_id=None):
    if request.user.location != "Y":
        return redirect("dangun_app:alert", alert_message=_("동네인증이 필요합니다."))

    post = None
    if post_id:
        try:
            post = PostProduct.objects.get(id=post_id)
        except PostProduct.DoesNotExist:
            pass

    return render(request, "dangun_app/write.html", {"post": post})


# 거래글수정 화면
def edit(request, id):
    post = get_object_or_404(PostProduct, id=id)
    if post:
        post.description = post.description.strip()
    if request.method == "POST":
        post.title = request.POST["title"]
        post.price = request.POST["price"]
        post.description = request.POST["description"]
        post.location = request.POST["location"]
        if "thumbnail" in request.FILES:
            post.thumbnail = request.FILES["thumbnail"]
        post.save()
        return redirect("dangun_app:trade_post", pk=id)

    return render(request, "dangun_app/write.html", {"post": post})


# 포스트 업로드
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 임시 저장
            post.author_id = request.user.id
            post.username = request.user.nickname  # 작성자 정보 추가 (이 부분을 수정했습니다)
            post.chat_id = uuid.uuid4().int & (1 << 63) - 1  # chat_id 부여
            post.save()  # 최종 저장
            return redirect("dangun_app:trade_post", post_id=post.pk)  # 저장 후 상세 페이지로 이동
        else:
            print(form.errors)  # 에러출력추가
    else:
        form = PostForm()
    return render(request, "dangun_app/trade_post.html", {"form": form})


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


# 물품 상세보기 페이지
def trade_post(request, post_id):
    # 포스트 id 번호를 불러옮
    post = get_object_or_404(PostProduct, id=post_id)
    if request.method == "POST":
        # html에서 delete-button name의 인풋을 눌러서 작동
        if "delete-button" in request.POST:
            post.delete()
            # 포스트페이지로 가는게 맞아서 나중에 바꿀것
            # return redirect('dangun_app/trade')
            return render(request, "dangun_app/main_test.html")
    #  조회수 증가
    post.view += 1
    post.save()

    context = {
        "post": post,
    }

    return render(request, "dangun_app/trade_post_test.html", context)


@login_required
def chatroom_list(request):
    # 채팅방 리스트 중 하나를 클릭했을 경우
    # if request.method == "POST":
    #     chatroom_id = request.

    # chat 화면을 처음 들어왔을 경우 채팅방 리스트를 뿌려줌
    user = request.user

def get_chatrooms_context(user):
    # 현재 로그인한 사용자가 chat_host 또는 chat_guest인 ChatRoom을 검색
    chatrooms = ChatRoom.objects.filter(Q(chat_host=user.id) | Q(chat_guest=user.id))

    # 최종적으로 넘겨줄 결과 chatroom 리스트 초기화
    chatrooms_context = []

    # 각 chatroom에 대해 필요한 정보 가져옴
    for chatroom in chatrooms:
        # 채팅 상대 정보
        if chatroom.chat_host == user.id:
            chat_partner = CustomUser.objects.get(id=chatroom.chat_guest)
        else:
            chat_partner = CustomUser.objects.get(id=chatroom.chat_host)

        # 상품
        product = PostProduct.objects.get(id=chatroom.product_id)

        # 마지막 주고 받은 메시지
        last_message = Message.objects.filter(chatroom_id=chatroom.id).order_by("-sent_at").first()

        result = {
          
            'chatroom' : chatroom, # 채팅방 정보
            'chat_partner' : chat_partner, # 채팅 상대방의 정보
            'product' : product, # 상품 정보
            'message' : last_message # 마지막 메시지 정보

        }

        chatrooms_context.append(result)
    
    return chatrooms_context


@login_required
def chatroom_list(request):
    user = request.user
    
    # 참여하고 있는 채팅방 목록 및 관련 정보 불러오기
    chatrooms_context = get_chatrooms_context(user)
    
    return render(request, 'dangun_app/chat.html', {'chatrooms' : chatrooms_context})


@login_required
def chatroom(request, chatroom_id):
    user = request.user

    # 참여하고 있는 채팅방 목록 및 관련 정보 불러오기
    chatrooms_context = get_chatrooms_context(user)
    
    # 클릭한 채팅방 및 채팅 상대방에 대한 정보
    selected_chatroom = ChatRoom.objects.get(id=chatroom_id)
    if selected_chatroom.chat_host == user.id:
        chat_partner = CustomUser.objects.get(id=selected_chatroom.chat_guest)

    # 채팅 상대 정보
    chatroom = ChatRoom.objects.get(id=chatroom_id)

    if chatroom.chat_host == user.id:
        chat_partner = CustomUser.objects.get(id=chatroom.chat_host)

    else:
        chat_partner = CustomUser.objects.get(id=selected_chatroom.chat_host)

    # 어떤 상품에 대한 채팅방인지
    product = PostProduct.objects.get(id=selected_chatroom.product_id)

    # 주고받은 채팅(메시지) 기록
    messages = Message.objects.filter(chatroom=chatroom_id).order_by('sent_at')

    # WebSocket 연결을 위한 주소
    ws_path = f"/ws/chat/{selected_chatroom.id}"

    # 템플릿에 전달할 데이터 정의
    context = {
        'chatrooms' : chatrooms_context,
        "selected_chatroom" : selected_chatroom,
        "product" : product,
        "chat_partner" : chat_partner,
        "messages" : messages,
        "ws_path" : ws_path,
    }

    return render(request, "dangun_app/chat.html", context)

