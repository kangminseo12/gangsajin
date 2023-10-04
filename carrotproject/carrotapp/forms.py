from django import forms
from .models import PostProduct, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = PostProduct
        fields = ["title", "price", "description", "location", "thumbnail"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': '',  # 'text' 필드의 라벨을 빈 문자열로 설정
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'form-text',
            'rows': '4',
            'cols': '100',
        })
