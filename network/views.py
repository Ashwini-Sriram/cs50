from genericpath import exists
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Posts, Followers


def index(request):
    if request.method == "POST":
        pst = Posts()
        pst.user = request.user
        pst.post = request.POST['post_content']
        pst.date_time = datetime.now()
        pst.save()
        return HttpResponseRedirect(reverse("index"))
    all_posts = Posts.objects.all().order_by('-date_time')
    return render(request, "network/index.html",{"posts":all_posts})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request,user_id):
    follower = User.objects.get(pk=request.user.id)
    following = User.objects.get(pk=user_id)
    if request.method=="POST":
        if request.POST['perform']=="Follow":
            Followers.objects.create(user_id=User.objects.get(pk=user_id), followed_user=request.user)
            following.followers_count+=1
            following.save()
            follower.following_count+=1
            follower.save()
        else:
            Followers.objects.filter(Q(user_id=user_id)&Q(followed_user=request.user.id)).delete()
            following.followers_count -= 1
            following.save()
            follower.following_count -= 1
            follower.save()
            
        return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))
    user = User.objects.get(pk=user_id)  
    posts = Posts.objects.filter(Q(user=user_id)).order_by('-date_time')
    followers_list=user.following.all()
    followers_l=[]
    for follower in followers_list:
       followers_l.append(getattr(follower,"followed_user"))
    
    return render(request, "network/profile.html",{"poster":user,"posts":posts,"followers":followers_l})


def following(request):
    user = User.objects.get(pk=request.user.id)
    following_list = user.followers.all()
    following_l = []
    for follower in following_list:
      f_id= getattr(follower, "user_id").id
      following_l.append(f_id)

    all_posts = Posts.objects.filter(user__in=following_l).order_by('-date_time')
    return render(request, "network/following.html", {"posts": all_posts})
