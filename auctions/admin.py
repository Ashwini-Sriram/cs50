from django.contrib import admin
from .models import User, AuctionListings, Bid, Comment, Categories


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Categories)
