from django.contrib import admin
from django import forms

from ckeditor_uploader.fields import RichTextUploadingField

from .models import Post, Category


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=RichTextUploadingField())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


admin.site.register(Post)
admin.site.register(Category)
