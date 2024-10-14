from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from .models import User, Listing, Bid, Comment, Category

def addWatchlist(request,listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse('shows', args=[listing_id]))

def removeWatchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse('watchlist'))

@login_required(login_url='login', redirect_field_name=None)
def showWatchlist(request):
    return render(request, 'auctions/watchlist.html',{
        'listings':Listing.objects.filter(watchlist=request.user)
    })


def closeBid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.status=False

    listing.save()

    return HttpResponseRedirect(reverse('listing'))

def addComment(request, listing_id):
    if request.method =='POST':
        comment = request.POST['comment']
        user = request.user
        listing = Listing.objects.get(id=listing_id)

        if (comment!=' '):
        

            newComment=Comment(
                user = user,
                comment = comment,
                listing = listing
            )

            newComment.save()
    return HttpResponseRedirect(reverse("shows", args=[listing_id]))

@login_required(login_url='login', redirect_field_name=None)
def listing(request):
    return render(request, 'auctions/listing.html',{
        'listings':Listing.objects.filter(user=request.user)
    })

@login_required(login_url='login', redirect_field_name=None)
def addListing(request):
    if(request.method == 'POST'):
        item = request.POST['item_name']
        desc = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        img_url = request.POST['imageurl']
        user = request.user

        if int(price)<0:
            return render(request, "auctions/addListing.html",{
            'categories':Category.objects.all(),
            'error_price':'the price should positive integer'
        })

        categoryData = Category.objects.get(category_name=category)

        bid = Bid(bid=int(price), user=user, time=datetime.datetime.now())
        bid.save()

        new_listing = Listing(
            user=user,
            item_name = item,
            description = desc,
            price = bid,
            category = categoryData,
            img_url = img_url,
            status = True
        )

        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/addListing.html",{
            'categories':Category.objects.all()
        })

def addBid(request, listing_id):
    bid_price = request.POST['bid_price']
    listing = Listing.objects.get(id=listing_id) #cari barang yg sedang ditawae

    if int(bid_price)> listing.price.bid and int(bid_price)>0:

        new_bid = Bid(user=request.user, bid=int(bid_price))
        listing.price = new_bid
        
        new_bid.save()
        listing.save()
        listing.watchlist.add(request.user)
    else:
        error_message = 'your bid too low'
        return render(request, 'auctions/show.html', {
            'error_message': error_message,
            'listing':listing,
            'comment': Comment.objects.filter(listing=listing_id)
            })

    return HttpResponseRedirect(reverse("shows", args=[listing_id]))

@login_required(login_url='login', redirect_field_name=None)
def showList(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing_id)
    return render(request, 'auctions/show.html',{
        'listing' : listing,
        'watchlists':listing.watchlist.all(),
        'comments' : comments,
    })




def index(request):
    return render(request, "auctions/index.html", {
        'listings':Listing.objects.all()
    })


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

