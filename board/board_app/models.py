from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.create_time} {self.title}: {self.content[:5]}...'


class Responses(models.Model):
    text = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

