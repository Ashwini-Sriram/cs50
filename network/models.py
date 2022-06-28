from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_count=models.IntegerField(null=True,default=0)
    following_count = models.IntegerField(null=True,default=0)

class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    id = models.AutoField(primary_key=True)
    post = models.CharField(max_length=256)
    likes = models.IntegerField(null=True,default=0)
    date_time = models.DateTimeField()

class Followers(models.Model):
    class Meta:
        unique_together = (('user_id', 'followed_user'),)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

  
