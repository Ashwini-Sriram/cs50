from pyexpat import model
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category_name = models.CharField(max_length=128, default="Not Listed")

    def __str__(self):
        return self.category_name


class AuctionListings(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lists")
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    img_url = models.CharField(max_length=128)
    desc = models.CharField(max_length=256)
    starting_bid = models.FloatField(max_length=64)
    watchlist_users = models.ManyToManyField(
        User, blank=True, related_name="watchlist")
    highest_bid = models.FloatField(max_length=64, blank=True, default=0.00)
    user_hbid = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    category = models.ForeignKey(
        Categories, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bid(models.Model):
    class Meta:
        unique_together = (('list_id', 'user_id'),)
    list_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField(max_length=64, blank=True)
    # same as highest bid just a reference
    current_bid = models.FloatField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} : {self.list_id}"


class Comment(models.Model):
    list_c = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    user_c = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    date_time = models.DateTimeField()



