from django.contrib import admin
from .models import User,AuctionListings,Bid

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(AuctionListings)
admin.site.register(Bid)

