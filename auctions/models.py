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

    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.category} {self.starting_bid} {self.url} {self.date} {self.listing_owner} "


class ActiveListings(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)


class Bids(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=99, default=None)
    current_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date = models.DateTimeField(default=now,blank=True)
    def __str__(self):
        return f"{self.listing_id} {self.user_id} {self.current_bid} "
   

class Comments(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=99, default=None)
    comment = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=now, blank=True)


class Watchlist(models.Model):

    user_id = models.CharField(max_length=99, default=None)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.id} {self.listing}" 
    

class Categories(models.Model):

    category = models.CharField(max_length=99, default=None)

    def __str__(self):
        return f"{self.category}" 
