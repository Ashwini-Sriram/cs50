from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=64,unique=True)
    img_url=models.CharField(max_length=128)
    desc=models.CharField(max_length=256)
    starting_bid=models.FloatField(max_length=64)
    watchlist_users = models.ManyToManyField(User,blank=True,related_name="watchlist")
    highest_bid = models.FloatField(max_length=64)
    user_hbid= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name 

class Bid(models.Model):
    unique_together = (('list_id', 'user_id'),)
    list_id=models.ForeignKey(AuctionListings,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    bid = models.FloatField(max_length=64,blank=True)
    current_bid =models.FloatField(max_length=64)



     


  

    
        

    

