from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Blog(models.Model):
    blog_title = models.CharField(max_length=100, unique=True)
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    post_title = models.CharField(max_length=100, unique=True)
    post_content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_content = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
