from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.create_listings , name ="createListings"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("listings/<str:list_id>",views.listings,name="listings")
]
