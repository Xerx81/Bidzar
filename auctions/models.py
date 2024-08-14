from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    categs = models.CharField(max_length=50)

    def __str__(self):
        return self.categs

class Listings(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.FloatField()
    image = models.CharField(max_length=2048, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_category")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")
    active = models.BooleanField(default=True)
    time =  models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing")

    def __str__(self):
        return f"{self.commenter} on {self.listing}"
    
class Bid(models.Model):
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_listing")

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.listing}"

