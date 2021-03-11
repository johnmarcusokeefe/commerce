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
        # need to filter active listings only
        listings = Listings.objects.filter(active_flag=True)

    else:
        listings = Listings.objects.filter(category=filter.lower()).filter(active_flag=True)
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

#
# categories with argument
#
def categories(request):

    # do a listing count per category
    listings = Listings.objects.filter(active_flag=True)
    categories = Categories.objects.all()
    # create a dictionary of category keys at 0
    cat_count = {}
    for c in categories:
        cat_count[c.category.lower()] = 0
    # tallies categories/ have to remove all not active
    for l in listings:
        cat_count[l.category] += 1

    
    return render(request, "auctions/categories.html", {
               'cat_count': cat_count
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


#close listing
def endbid(request, id):
    
    listing = Listings.objects.get(id=id)
    all_bids = Bids.objects.filter(listing_id=id)
    if not all_bids:
        bids_so_far = 0
    else:
        bids_so_far = all_bids.count()
    highest = listing.starting_bid

    highest_owner = ""
    for b in all_bids:
        if b.current_bid + 1 > highest:
            highest = b.current_bid
            #highest_owner = b.user_id
            
    # tests if bids are greater than 0 before closing otherwise todo prompt if wants closed no bids
    if bids_so_far > 0:
        # get user of highest bid
        Bids.objects.filter(listing_id=id).filter(current_bid=highest).update(winning_bid=True)
        Listings.objects.filter(id=id).update(active_flag=False)
        messages.add_message(request, messages.INFO, 'Bidding is closed')
    else:
        # alert message to close
        Bids.objects.filter(listing_id=id).filter(current_bid=highest).update(winning_bid=True)
        Listings.objects.filter(id=id).update(active_flag=False)
        messages.add_message(request, messages.ERROR, 'You have closed the listing with 0 bids')
    
    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


# function to process a listings detail
def listing(request, id):
    # get the listing of the id
    listing = Listings.objects.get(id=id)
    user_id = request.user
    listing_id = Listings(id=id)

    #
    # set currently highest bid
    #
    all_bids = Bids.objects.filter(listing_id=listing_id)
    bids_so_far = all_bids.count
    highest = listing.starting_bid
    highest_owner = ""
    for b in all_bids:
        if b.current_bid + 1 > highest:
            highest = b.current_bid
            highest_owner = b.user_id 

    # get bid form data
    bidform = BidForm(request.POST)
    # process bid
    bid_status = Bids.objects.filter(listing_id=id).filter(winning_bid=True)
    
    # user id of winning bid
    winner = False
    if user_id == bid_status:
        winner = True;
        
    # sets the bid display status
    if bid_status:
        bid_status = True
    else: 
        bid_status = False

    if request.method == 'POST' and bidform.is_valid():
    # without any bids the bid is loaded with the supplied minimum bid
        # get current bid 
        
        new_bid = bidform.cleaned_data['bid']
        if new_bid > highest:
            b = Bids(listing_id=listing_id, user_id=user_id, current_bid=new_bid)
            b.save()
            highest = new_bid
            messages.add_message(request, messages.INFO, 'Bid accepted')
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
        else:
            # give error
            messages.add_message(request, messages.ERROR, 'Enter amount $'+str(highest+1)+" or higher")
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
   

    #
    # get comment form data
    #
    commentform = CommentForm(request.POST)
    # process comments    
    if request.method == 'POST' and commentform.is_valid():    
 
        comment = commentform.cleaned_data['comment']
        c = Comments(listing_id=listing_id, user_id=user_id, comment=comment)
        c.save()
        # reverse stops post data being resaved
        return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))

    
    # setting watchlist option
    if Watchlist.objects.filter(user_id=request.user.id, listing_id=listing_id):
        watch_flag = "watching"
    else:
        watch_flag = "notwatching"
    
    # count of watchlist
    watch_count = Watchlist.objects.filter(listing=id).count()

    
    # default render pages dependant on login status
    comments = Comments.objects.filter(listing_id=id)
    if request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
                'listing': listing,
                'watch_flag': watch_flag,
                'bidform': BidForm(),
                'current_bid': highest,
                'bids_so_far': bids_so_far,
                'highest_owner': highest_owner,
                'commentform': CommentForm(),
                'comments': comments,
                'user_id': user_id,
                'watch_count': watch_count,
                'winner': winner,
                'bid_status': bid_status,
                'userauthenticated': True
            })
    else:
        return render(request, "auctions/listing.html", {
               'listing': listing,
               'current_bid': highest,
               'bids_so_far': bids_so_far,
               'comments': comments,
               'bid_status': bid_status,
               'userauthenticated': False
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
            user_instance = User(id=request.user.id)
            get_watch_item = Watchlist.objects.filter(user_id=user_instance, listing=listing_instance)
            if get_watch_item:
                get_watch_item.delete() # line 1
            else:
                w = Watchlist(user_id=user_instance, listing=listing_instance)
                w.save()
        
            return HttpResponseRedirect(reverse("listing", kwargs={'id': listing}))
    # redirect to message if watchlist is selected while not logged in
    else:
        return render(request, "auctions/watchlist.html",  {
                # listings filtered from watchlist
                'login' : "none"
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
                "message": "Invalid username and/or password!"
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
