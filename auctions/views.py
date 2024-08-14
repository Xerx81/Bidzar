from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, Listings, Comments, Bid


def index(request):

    # send all active objects in listings to html page
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(active=True)
    })


@login_required(login_url='/login')
def closed_listings(request):

    # send all closed objects in listings to html page
    return render(request, "auctions/closed.html", {
        "listings": Listings.objects.filter(active=False)
    })


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = float(request.POST["price"])
        description = request.POST["description"]
        image = request.POST["image"]
        seller = request.user
        time = datetime.now()
        try:
            category = request.POST["category"]

            # Get category data from Categories model
            categ = Categories.objects.get(categs=category)
        except:
            categ = None

        # Add new listing data to Listings model
        listing = Listings(
            title=title,
            price=price,
            description=description,
            image=image,
            category=categ,
            seller=seller,
            time = time
        )
        listing.save()

        # Redirect to active listing page
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "categories": Categories.objects.all()
    })
     

def listing(request, id):

    # Get listing data of given title
    listing = Listings.objects.get(pk=id)

    # Get all comments for the listing
    comments = listing.comment_listing.all()  

    # Number of bids so far
    total_bids = listing.bid_listing.count()

    # Get the name of highest bidder after closing auction
    bid = Bid.objects.filter(listing=id)
    if bid:
        max_bid = bid.order_by('-amount').first()
        winner = max_bid.bidder
    else:
        winner = "None"    

    # Check if user has already watchlisted the listing
    watchlisted = False
    if request.user in listing.watchlist.all():
        watchlisted = True

    if request.method == 'POST':
        """ Add to watchlist """
        watchlist_info = request.POST["watchlist"]

        # Add user to the watchlist of current listing
        if watchlist_info == "Watchlist":
            user = request.user
            listing.watchlist.add(user)
            return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
        
        # Remove user from the watchlist of current listing
        else:
            user = request.user
            listing.watchlist.remove(user)
            return HttpResponseRedirect(reverse("listing", args=(listing.id, )))

    return render (request, "auctions/listing.html", {
        "listing": listing,
        "watchlisted": watchlisted,
        "comments": comments,
        "total_bids": total_bids,
        "winner": winner
    })



@login_required(login_url='/login')
def bid(request, id):

     # Get listing data of given title
    listing = Listings.objects.get(pk=id)

    # Get all comments for the listing
    comments = listing.comment_listing.all()  

    # Check if user has already watchlisted the listing
    watchlisted = False
    if request.user in listing.watchlist.all():
        watchlisted = True

    if request.method == "POST":

        # Get base price entered by seller
        starting_price = listing.price
        new_bid = float(request.POST["bid"])

        # Check if bid is greater than base price or previous bid
        if new_bid > starting_price:

            # Save bid to the database
            user = request.user
            save_bid = Bid(
                amount=new_bid,
                bidder=user,
                listing=listing
            )
            save_bid.save()

            # Update the price of the listing
            listing.price = new_bid
            listing.save()
            

            # Number of bids so far
            total_bids = listing.bid_listing.count()

            return render(request, "auctions/listing.html", {
                "message": "successful",
                "listing": listing,
                "comments": comments,
                "watchlisted": watchlisted,
                "total_bids": total_bids
            })
        
        else:
            return render(request, "auctions/listing.html", {
                "message": "unsuccessful",
                "listing": listing,
                "comments": comments,
                "watchlisted": watchlisted,
                "total_bids": listing.bid_listing.count()
            })


def close_auctions(request, id):
    if request.method == "POST":
        if request.POST["close"]:

            # Deactivate the listing
            listing = Listings.objects.get(pk=id)
            listing.active = False
            listing.save()

            # Redirect to active listing page
            return index(request)


@login_required(login_url='/login')
def show_watchlist(request):

    # Get all listings which are watchlisted by current user
    user = request.user
    listings = user.user_watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url='/login')
def show_categories(request):

    if request.method == "POST":
        form_category = request.POST["category"]
        categ = Categories.objects.get(categs=form_category)

        # Get all listings under the category that user entered
        listings = Listings.objects.filter(category=categ, active=True)

        return render(request, "auctions/index.html", {
            "listings": listings,
            "category": form_category
        })

    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


@login_required(login_url='/login')
def comments(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]

        if not comment:
            return HttpResponseRedirect(reverse("listing", args=(id, )))
        
        # Get current user and listing 
        user = request.user
        listing = Listings.objects.get(pk=id)

        # Save data to database
        save_comment = Comments(
            comment=comment,
            commenter=user,
            listing=listing
        )
        save_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))


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
