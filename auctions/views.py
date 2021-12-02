from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.decorators import login_required

from .models import User, AuctionList, Bid, Comment

class createListingForm(forms.Form):
    category_choices = AuctionList.category_choices()

    title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    description = forms.CharField(label="Description", 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': '3'
        }))
    start_bid = forms.IntegerField(label="Start Bid", required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'min': '1'
        }))
    image_url = forms.CharField(label="Image Link", max_length=500, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    category = forms.ChoiceField(label="Category",
            choices=category_choices,
            widget=forms.Select(attrs={
            'class': 'form-control'
        }))

@login_required(login_url="login")
def index(request):
    listing = AuctionList.objects.all()
    bid = Bid.objects.all()
    if bid:
        winner = bid.order_by('-bid')[0]
        return render(request, "auctions/index.html", {
                "listing": listing.order_by("-status", "-id"),
                "winner": winner.user.username
            })
    else:
        return render(request, "auctions/index.html", {
                "listing": listing.order_by("-status", "-id")
            })

@login_required(login_url="login")
def listing(request, item_id):
    item = AuctionList.objects.get(pk=item_id)
    comment = Comment.objects.filter(item=item).order_by("-id")

    # If the bid exist for this item
    if Bid.objects.filter(item = item, user = request.user).exists():
        bid = Bid.objects.get(item = item, user = request.user)
        return render(request, "auctions/listing.html", {
                'item': item,
                'current_user': request.user,
                'bid': bid,
                'comments': comment
            })

    # If the bid is not exist for this item
    else:
        return render(request, "auctions/listing.html", {
                'item': item,
                'current_user': request.user,
                'watchlist': False,
                'comments': comment
            })

@login_required(login_url="login")
def bidding(request, item_id):
    item = AuctionList.objects.get(pk=item_id)
    if request.method == "POST":

        # Add new bid
        if not Bid.objects.filter(item = item, user = request.user).exists():
            bidding = Bid(
                item = AuctionList.objects.get(pk=item_id),
                user = User.objects.get(pk=request.user.id),
                bid = int(request.POST["bid"]),
                watchlist = True
                )
            item.start_bid = int(request.POST["bid"])
            bidding.save()
            item.save()

        # Update existing bid
        else:
            bid = Bid.objects.get(item = item, user = request.user)
            bid.bid = int(request.POST["bid"])
            item.start_bid = int(request.POST["bid"])
            bid.save()
            item.save()

        return HttpResponseRedirect(reverse("listing", args=(item_id,)))

@login_required(login_url="login")
def watchlist(request, item_id):
    item = AuctionList.objects.get(pk=item_id)
    if request.method == "POST":

        # Add to watchlist without bid
        if not Bid.objects.filter(item = item, user = request.user).exists():
            watch = Bid(
                item = AuctionList.objects.get(pk=item_id),
                user = User.objects.get(pk=request.user.id),
                watchlist = True
            )
            watch.save()

        # Alter watchlist in existing bid    
        else:
            watch = Bid.objects.get(item = item, user = request.user)
            if not watch.watchlist:
                watch.watchlist = True
            else:
                watch.watchlist = False
            watch.save()
    return HttpResponseRedirect(reverse("listing", args=(item_id,)))

@login_required(login_url="login")
def close_bid(request, item_id):

    # Turn item status to False
    item = AuctionList.objects.get(pk=item_id)
    if request.method == "POST":
        item.status = False
        item.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url="login")
def comment(request, item_id):
    if request.method == "POST":
        item = AuctionList.objects.get(pk=item_id)
        comment = Comment(
            item = item,
            user = request.user,
            comment = request.POST["comment"]
            )
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=(item_id,)))

@login_required(login_url="login")
def view_watchlist(request):

    # Get the items on watchlist
    bids = Bid.objects.filter(user = request.user, watchlist = True).order_by("-id") 
    return render(request, "auctions/watchlist.html", {
            "username": request.user.username,
            "bids": bids
        })

@login_required(login_url="login")
def category(request):
    return render(request, "auctions/category.html", {
        "listing": AuctionList.category_choices()
        })

@login_required(login_url="login")
def category_name(request, name):

    # Display item in the "name" category
    listing = AuctionList.objects.filter(category = name)
    return render(request, "auctions/category_name.html", {
        "listing": listing,
        "name": name
        })

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = createListingForm(request.POST)
        if form.is_valid():

            # Get link for default image
            image_url=''
            if not form.cleaned_data['image_url']:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"
            else:
                image_url = form.cleaned_data['image_url']

            listing = AuctionList(
                user = request.user,
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                start_bid = form.cleaned_data['start_bid'],
                image_url = image_url,
                category = form.cleaned_data['category']
                )
            listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = createListingForm()
        return render(request, "auctions/create_listing.html", {
                'form': form
            })
    # TODO:
    # - Prompt error when use enter invalid price
    # - Have an empty category for defaul choice

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
