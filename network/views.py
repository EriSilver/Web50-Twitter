from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import *
from .funcs import *


def index(request):
    return HttpResponseRedirect(reverse("allposts", args=[1]) )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("allposts", args=[1]) )
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("allposts", args=[1]) )


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
        return HttpResponseRedirect(reverse("allposts", args=[1]) )
    else:
        return render(request, "network/register.html")

def allposts(request, apage):
    postss = posts.objects.all().order_by("-pdate")
    postss, thepage, p = getposts(apage, postss)
    if thepage == "x":
        return render(request, "network/index.html", {
            "msg": "Page does not exist", 
            "pages": range(1, p + 1)
        })
    
    return render(request, "network/index.html", {
        "posts": postss.page(thepage),
        "theliked": request.user.towork() if request.user.username else [],
        "pages": range(1, p + 1)
    })

def newpost(request):
    if request.method == "POST":
        data = dict(request.POST)
        #print(data)
        post = data["thenewpost"][0].lstrip().rstrip()
        if not post:
            msg = "The post should not consist of just spaces."
        elif len(post) > 280:
            msg = "The maximum length is 280 charachters."
        else:
            user = User.objects.get(username=request.user.username)
            #print(user)
            item = posts(puser=user, post=post)
            item.save()
            post = ""
            msg = ""

        postss = posts.objects.all().order_by("-pdate")
        postss, thepage, p = getposts(1, postss)
        if thepage == "x" and p == "x":
            return render(request, "network/index.html", {
                "msg": "Page does not exist"
            })

        return render(request, "network/index.html", {
            "posts": postss.page(thepage),
            "pages": range(1, p + 1),
            "theliked": User.objects.get(username=request.user.username).towork(),
            "postvalue": post,
            "msg": msg,
        })
    else:
        return HttpResponseRedirect(reverse("allposts", args=[1]))

def editpost(request):
    data = json.loads(request.body)
    p = posts.objects.get(id=data["id"])
    p.post = data["value"]
    p.save()
    return HttpResponse(status=204)

def likepost(request):
    data = json.loads(request.body)
    user = User.objects.get(username=request.user.username)
    post = posts.objects.get(id=data["id"])
    like = data["like"]
    if like:
        post.likes.add(user)
        thelist = user.towork()
        thelist.append(data["id"])
        user.tojsondumps(thelist)
    else:
        post.likes.remove(user)
        thelist = user.towork()
        thelist.remove(data["id"])
        user.tojsondumps(thelist)
    return HttpResponse(status=204)


def followingposts(request, apage):
    if not request.user.username:
        return HttpResponseRedirect(reverse("login"))
    
    postss = list(posts.objects.all().order_by("-pdate"))

    ulist = request.user.following.values_list("id", flat=True)
    count = 0
    for p in range(len(postss)):
        if postss[p-count].puser.id not in ulist:
            postss.pop(p-count)
            count += 1
    
    postss, thepage, p = getposts(apage, postss)

    if thepage == "x":
        return render(request, "network/index.html", {
            "msg": "Page does not exist", 
            "pages": range(1, p + 1),
            "following": True
        })
    
    return render(request, "network/index.html", {
        "posts": postss.page(thepage),
        "theliked": request.user.towork(),
        "pages": range(1, p + 1),
        "following": True
    })
    
def user(request, user, apage):
    uuser = User.objects.get(username=user)
    postss = uuser.thepuser.all().order_by("-pdate")
    postss, thepage, p = getposts(apage, postss)
    followtrue = False
    print(request.user)
    if request.user.username:
        followtrue = user in request.user.following.values_list("username", flat=True) 

    return render(request, "network/user.html", {
        "posts": postss.page(thepage),
        "theliked": request.user.towork() if request.user.username else [],
        "pages": range(1, p + 1),
        "title" : "Your" if request.user.username == user else f"{user}\'s",
        "same" : request.user.username == user,
        "pageuser": uuser,
        "followtrue": followtrue
    })

def followuser(request):
    data = json.loads(request.body)
    if data["follow"] :
        request.user.following.add(User.objects.get(username=data["pageuser"]))
    else:
        request.user.following.remove(User.objects.get(username=data["pageuser"]))

    return HttpResponse(status=204)
