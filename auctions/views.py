# /Users/johnokeefe/desktop/cs50/project_2/commerce

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Categories, UserListings
from .forms import ListingForm

# index displays listings
def index(request):
    #print(request.user.username)
    # todo: get listings from database 
    # only display active listings

    listings = Listings.objects.all()
    # testing
    #listing_id = Listings.objects.last()
    #print(listing_id.id)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


# render a listing
def display_listing(request, id):
    # get the listing of the id
    listing = Listings.objects.get(id=id)
    print(listing)
    return render(request, "auctions/display_listing.html", {
               'listing': listing
            })


# renders the form to create a new listing
def create_listing(request):
    message = False
    # post would be a call from the listing input form
    form = ListingForm
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            cat = form.cleaned_data['category']
            bid = form.cleaned_data['min_bid']
            url = form.cleaned_data['media_url']
            l = Listings(title=title, description=desc, category=cat, starting_bid=bid, url=url)
            l.save()
            user_id = request.user
            listing_id = Listings.objects.last().id
            ul = UserListings(user_id=user_id, listing_id=listing_id)
            ul.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        # render the input form
        return render(request, "auctions/create_listing.html", {
                "type": "createlisting",
                "message": message,
                "form": form
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
