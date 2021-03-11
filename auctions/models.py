# python3 manage.py makemigrations
# python3 manage.py migrate

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# added listing id
class User(AbstractUser):
    pass


class Listings(models.Model):

    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=100, default=None)
    category = models.CharField(max_length=50, default=None)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    url = models.URLField(max_length=200)
    date = models.DateTimeField(default=now,blank=True)
    listing_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.category} {self.starting_bid} {self.url} {self.date} {self.listing_owner}"

# by default the listing is added to bids with the starting bid0.23
class Bids(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    current_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    winning_bid = models.BooleanField(default=False)
    date = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return f"{self.listing_id} {self.user_id} {self.current_bid} {self.winning_bid} {self.date} "
   

class Comments(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.listing_id} {self.user_id} {self.comment} {self.date} "


class Watchlist(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.id} {self.listing} {self.date}" 
    

class Categories(models.Model):

    category = models.CharField(max_length=99, default=None)

    def __str__(self):
        return f"{self.category}" 
