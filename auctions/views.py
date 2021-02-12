# /Users/johnokeefe/desktop/cs50/project_2/commerce

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import Listings, Categories, Comments, Watchlist, Bids, User
from .forms import CreateListingForm, BidForm, CommentForm

# index displays listings
def index(request, filter="none"):
    
    current_page = "All"

    # add filter functionality none = all listings will be show
    if filter == "All" or filter == "none":
        listings = Listings.objects.all()
    else:
        listings = Listings.objects.filter(category=filter.lower())
        current_page = filter
       
    # load all categories
    categories = Categories.objects.all()
    
    
    # returns the homepage listings
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories,
        "filter": filter,
        "current_page": current_page
    })


# function to process a listings detail
def details(request, id):
    # get the listing of the id
    listing = Listings.objects.get(id=id)
    user_id = request.user
    listing_id = Listings(id=id)
    # need to check if a bid or a comment and process
    # set currently highest bid
    all_bids = Bids.objects.filter(listing_id=listing_id)
    highest = listing.starting_bid
    for b in all_bids:
        if b.current_bid + 1 > highest:
            highest = b.current_bid 

    # get bid form data
    bidform = BidForm(request.POST)
    # process bid
    if request.method == 'POST' and bidform.is_valid():
    # without any bids the bid is loaded with the supplied minimum bid
        # get current bid 
        new_bid = bidform.cleaned_data['bid']
        if new_bid > highest:
            b = Bids(listing_id=listing_id, user_id=user_id, current_bid=new_bid)
            b.save()
            highest = new_bid
            messages.add_message(request, messages.INFO, 'bid accepted')
        else:
            # give error
            messages.add_message(request, messages.ERROR, 'enter amount $'+str(highest+1)+" or higher")
            return HttpResponseRedirect(reverse('details', kwargs={'id': id}))

    # get comment form data
    commentform = CommentForm(request.POST)
    # process comments    
    if request.method == 'POST' and commentform.is_valid():    
 
        comment = commentform.cleaned_data['comment']
        c = Comments(listing_id=listing_id, user_id=user_id, comment=comment)
        c.save()
        # reverse stops post data being resaved
        return HttpResponseRedirect(reverse('details', kwargs={'id': id}))

    
    # setting watchlist option
    if Watchlist.objects.filter(user_id=request.user.id, listing_id=listing_id):
        watch_flag = "watching"
    else:
        watch_flag = "notwatching"
    
    
    # default render pages dependant on login status
    comments = Comments.objects.filter(listing_id=id)
    if request.user.is_authenticated:
        return render(request, "auctions/details.html", {
               'listing': listing,
               'watch_flag': watch_flag,
               'bidform': BidForm(),
               'current_bid': highest,
               'commentform': CommentForm(),
               'comments': comments,
               'userauthenticated': True
            })
    else:
        return render(request, "auctions/details.html", {
               'listing': listing,
               'current_bid': highest,
               'comments': comments,
               'userauthenticated': False
            })


# categories with argument
def categories(request):
    
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
               'categories': categories
            })


# watchlist
def watchlist(request, listing="none"):

    id = request.user.id

    if id != "none":
        if listing == "none":
            watchlist = Watchlist.objects.filter(user_id = id)
            
            # get the listings that are being watched
            return render(request, "auctions/watchlist.html",  {
                # listings filtered from watchlist
                'watchlist' : watchlist,
                'login': "yes"
            })
        # add item to watchlist and return to listings
        else:
            # add item to watchlist
            listing_instance = Listings(id=listing)
            get_watch_item = Watchlist.objects.filter(user_id=request.user.id, listing=listing_instance)
            if get_watch_item:
                get_watch_item.delete() # line 1
            else:
                w = Watchlist(user_id=id, listing=listing_instance)
                w.save()
        
            return HttpResponseRedirect(reverse("details", kwargs={'id': listing}))
    # redirect to message if watchlist is selected while not logged in
    else:
        return render(request, "auctions/watchlist.html",  {
                # listings filtered from watchlist
                'login' : "none"
            })


# renders the form to create a new listing
def create(request):
    message = False
    # post would be a call from the listing input form
    form = CreateListingForm()


    if request.method == 'POST':
        form = CreateListingForm(request.POST)
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
                "form": form,
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
            # if a user logs in from details it will go back to the details page
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
