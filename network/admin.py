from django.contrib import admin

from network.models import Posts, User, Followers

# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Followers)