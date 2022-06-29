import json
from genericpath import exists
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from requests import request
from .models import Likedposts, User,Posts, Followers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == "POST":
        pst = Posts()
        pst.user = request.user
        pst.post = request.POST['post_content']
        pst.date_time = datetime.now()
        pst.save()
        return HttpResponseRedirect(reverse("index"))
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        liked_posts = user.liked_posts.all()
        liked_l = []
        for liked_post in liked_posts:
          liked_l.append(getattr(liked_post, "post_liked"))
        all_posts = Posts.objects.all().order_by('-date_time')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {"posts": page_obj, "liked": liked_l})
    else:
        all_posts = Posts.objects.all().order_by('-date_time')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {"posts": page_obj})

    


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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{"poster":user,"posts":page_obj,"followers":followers_l})


def following(request):
    user = User.objects.get(pk=request.user.id)
    following_list = user.followers.all()
    following_l = []
    for follower in following_list:
      f_id= getattr(follower, "user_id").id
      following_l.append(f_id)
    


    all_posts = Posts.objects.filter(user__in=following_l).order_by('-date_time')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts": page_obj})



#API functions


@csrf_exempt
@login_required
def edit(request,post_id):
    try:
        post_obj = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    if request.method=="PUT":
        data = json.loads(request.body)
        post_obj.post=data['post']
        post_obj.save()
        return JsonResponse(post_obj.post, safe=False)

        #return JsonResponse(post_obj.serialize(),safe=False)


@csrf_exempt
@login_required
def like(request, post_id):
    try:
        post_obj = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data["like"]==True:
            Likedposts.objects.create(user_liked=request.user,post_liked=post_obj)
            post_obj.likes += 1
        elif post_obj.likes>0:
            Likedposts.objects.filter(Q(user_liked=request.user.id) & Q(
                post_liked=post_id)).delete()
            post_obj.likes -= 1
        post_obj.save()
        return JsonResponse(post_obj.likes, safe=False)

   
