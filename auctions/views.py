from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment

logged = False
username = ""

def index(request):
    return render(request, "auctions/index.html",{
        "listing" : Listing.objects.all(),
        "bids" : Bid.objects.all(),
        "comments" : Comment.objects.all()
    })

def item(request, item):
    lis = Listing.objects.filter(id = item).first()
    return render(request, "auctions/item_page.html", {
        "message": "Enter your bid",
        "item": item,
        "listing" : lis,
        "bids" : Bid.objects.filter(serial = Listing.objects.get(id = item)),
        "comments" : Comment.objects.all()    
    })


def place_bid(request, item):
    global logged
    global username
    if not logged:
        return render(request, "auctions/login.html", {
                "message": "Please login first."
            })
    else:
        amu = request.GET.get("q")
        lis = Listing.objects.get(id = item)
        if float(amu)<= Listing.objects.get(id = item).price:
            return render(request, "auctions/item_page.html", {
            "message": "Unsuccessful bid",
            "item": item,
            "listing" : lis,
            "bids" : Bid.objects.filter(serial = Listing.objects.get(id = item)),
            "comments" : Comment.objects.all()    
            })
        bid = Bid.objects.create(serial = Listing.objects.get(id = item), username = username, amt = amu)
        bid.save()
        lis.price = amu
        lis.save()
        return render(request, "auctions/item_page.html", {
            "message": "Successful bid",
            "item": item,
            "listing" : lis,
            "bids" : Bid.objects.filter(serial = Listing.objects.get(id = item)),
            "comments" : Comment.objects.all()    
        })

def create(request):
    return render(request, "auctions/create.html")

def createlist(request):
    lis = Listing.objects.create(title = request.POST.get("title"), image= request.POST.get("image"), price = request.POST.get("price"), description= request.POST.get("description"))
    lis.save()
    return render(request, "auctions/index.html",{
        "listing" : Listing.objects.all(),
        "bids" : Bid.objects.all(),
        "comments" : Comment.objects.all()
    })

def login_view(request):
    global logged
    global username
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            logged = True
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            username = ""
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    global logged
    global username
    logout(request)
    logged = False
    username = ""
    return HttpResponseRedirect(reverse("index"))


def register(request):
    global logged
    global username
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
        logged = True
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        username = ""
        return render(request, "auctions/register.html")