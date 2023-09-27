from django import forms
from .models import PostProduct


class PostForm(forms.ModelForm):
    class Meta:
        model = PostProduct
        fields = ["title", "price", "description", "location", "thumbnail"]
