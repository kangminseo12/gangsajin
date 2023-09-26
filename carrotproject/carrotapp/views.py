from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login

from .models import PostProduct
# Create your views here.


def main(request):
    return render(request, "dangun_app/main_test.html")


# 물품 상세보기 페이지
def trade_post(request,post_id):
    # 포스트 id 번호를 불러옮
    post = get_object_or_404(PostProduct,id=post_id)
    if request.method == 'POST':
        # html에서 delete-button name의 인풋을 눌러서 작동
        if 'delete-button' in request.POST:
            post.delete()
            # 포스트페이지로 가는게 맞아서 나중에 바꿀것
            # return redirect('dangun_app/trade')
            return render(request, "dangun_app/main_test.html")
    #  조회수 증가
    post.view +=1
    post.save()

    context ={
        "post" : post,
    }
    return render(request,"dangun_app/trade_post_test.html", context)