from datetime import datetime
from tkinter import W
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from matplotlib.pyplot import title
from requests import request
from django.db.models import Q

from .forms import createListings
from .models import User, AuctionListings, Bid, Comment, Categories


def index(request):
    all_data = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {"data": all_data})


def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listings(request):
    if request.method == "POST":
        al = AuctionListings()
        al.user = request.user
        al.name = request.POST['title']
        al.desc = request.POST['text_desc']
        al.starting_bid = request.POST['start_bid']
        al.img_url = request.POST['img_url']
        al.closed = False
        al.category = Categories.objects.get(pk=request.POST["category"])
        al.save()
        all_data = AuctionListings.objects.all()
        return render(request, "auctions/index.html", {"data": all_data})
    category_l = Categories.objects.all()
    return render(request, "auctions/create_listings.html", {"form": createListings, "categories": category_l})


def listings(request, list_id):

    if request.method == "POST" and request.POST["form_n"] == "watchlist":
        al2 = AuctionListings.objects.get(pk=request.POST["item_id"])
        if request.POST["act"] == "Add to Watch List":
            al2.watchlist_users.add(
                User.objects.get(pk=request.POST["user_id"]))
        else:
            al2.watchlist_users.remove(
                User.objects.get(pk=request.POST["user_id"]))
        al2.save()
        al = AuctionListings.objects.get(pk=list_id)
        user = User.objects.get(pk=request.user.id)
        list_items = user.watchlist.all()
        return render(request, "auctions/listings.html", {"list_id": list_id, "item": al, "wishlist": list_items})

    # placing a bid
    elif request.method == "POST" and request.POST["form_n"] == "bid":

        if Bid.objects.filter(Q(list_id=list_id) & Q(user_id=request.user.id)):
            b = Bid.objects.filter(Q(list_id=list_id) &
                                   Q(user_id=request.user.id))[0]
            al = AuctionListings.objects.get(pk=list_id)
            b.bid = float(request.POST["bid_value"])
            if(al.highest_bid and b.bid < al.highest_bid):
                return HttpResponse("Error your bid is lower than the bids present")
            b.current_bid = b.bid if al.starting_bid < b.bid else al.starting_bid
            al.highest_bid = b.current_bid
            if al.starting_bid < b.bid:
                al.user_hbid = request.user
            al.save()
            b.save()
            url = reverse("listings",kwargs= {"list_id": list_id})
            return HttpResponseRedirect(url)

        else:
            b = Bid()
            b.user_id = request.user
            b.list_id = AuctionListings.objects.get(pk=list_id)
            al = AuctionListings.objects.get(pk=list_id)
            b.bid = float(request.POST["bid_value"])
            if(al.highest_bid and b.bid < al.highest_bid):
                return HttpResponse("<h1>Error your bid is lower than the bids present</h1>")
            elif(b.bid<al.starting_bid):
                return HttpResponse("<h1>Error : Lower than the starting bid </h1>")
            b.current_bid = b.bid if al.starting_bid <= b.bid else al.starting_bid
            al.highest_bid = b.current_bid
            al.user_hbid = request.user
            al.save()
            b.save()
           # al = AuctionListings.objects.get(pk=list_id)
            url = reverse("listings",kwargs= {"list_id": list_id})
            return HttpResponseRedirect(url)

    elif request.method == "POST" and request.POST["form_n"] == "close":
        al = AuctionListings.objects.get(pk=list_id)
        al.closed = True
        al.save()
        url = reverse("listings",kwargs= {"list_id": list_id})
        return HttpResponseRedirect(url)

    elif request.method == "POST" and request.POST["form_n"] == "comment":
        c = Comment()
        al = AuctionListings.objects.get(pk=list_id)
        c.list_c = al
        c.user_c = request.user
        c.comment = request.POST["comment"]
        c.date_time = datetime.now()
        c.save()
        url = reverse("listings",kwargs= {"list_id": list_id})
        return HttpResponseRedirect(url)
       
    

    if request.user.is_authenticated:
        al = AuctionListings.objects.get(pk=list_id)
        user = User.objects.get(pk=request.user.id)
        list_items = user.watchlist.all()
        comments = Comment.objects.filter(list_c=list_id)
        return render(request, "auctions/listings.html", {"list_id": list_id, "item": al, "wishlist": list_items, "comments": comments})
    else:
        al = AuctionListings.objects.get(pk=list_id)
        comments = Comment.objects.filter(list_c=list_id)
        return render(request, "auctions/listings.html", {"list_id": list_id, "item": al, "comments": comments})



def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    list_items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"list": list_items})


def categories(request):
    category_l = Categories.objects.all()
    return render(request,"auctions/categories.html",{"categories":category_l})

def category(request,category_id):
    category = Categories.objects.get(pk=category_id)
    al=AuctionListings.objects.filter(Q(category=category))
    return render(request,"auctions/category.html",{"category":category,"list_items":al})