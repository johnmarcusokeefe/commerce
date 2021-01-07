# /Users/johnokeefe/desktop/cs50/project_2/commerce

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listings, Categories
from .forms import ListingForm, BidForm, CommentForm

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


#  listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
#  user_id = models.CharField(max_length=99, default=None)
#  bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
#  date = models.DateTimeField(default=now,blank=True)

# render a listing
def display(request, id):
    # get the listing of the id
    listing = Listings.objects.get(id=id)
    bidform = BidForm()
    commentform = CommentForm()
    bid = ""
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            # get current bid 
            # if it is add to bid model

        
    print(listing)
    return render(request, "auctions/display.html", {
               'listing': listing,
               'bidform': bidform,
               'bid': bid,
               'commentform': commentform
            })

# categories
def categories(request, filter=None):
    
    if filter == None:
        categories = Categories.objects.all()
        return render(request, "auctions/categories.html", {
               'categories': categories
            })
    else:
        category_listings = Listings.objects.filter(category=filter.lower())
        print("cat listings",category_listings)
        return render(request, "auctions/index.html", {
               'listings': category_listings,
               'filter': filter
            })


# categories
def watchlist(request):
    return render(request, "auctions/categories.html", {
               'title': 'watchlist'
            })


# renders the form to create a new listing
def create(request):
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
            username=request.user.get_username()
            user = User.objects.get(username=username)
            url = form.cleaned_data['media_url']
            l = Listings(title=title, description=desc, category=cat, starting_bid=bid, listing_owner=user, url=url)
            l.save()          
            return HttpResponseRedirect(reverse("index"))
    else:
        # render the input form
        return render(request, "auctions/create.html", {
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
