# python3 manage.py makemigrations
# python3 manage.py migrate

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# added listing id
class User(AbstractUser):
    pass


class Listings(models.Model):

    #default: id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=100, default=None)
    category = models.CharField(max_length=50, default=None)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    url = models.URLField(max_length=200)
    date = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.starting_bid} {self.url} {self.date}"


# added listing id
class UserListings(models.Model):
    
    user_id = models.CharField(max_length=50, default=None)
    listing_id = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f"{self.user_id} {self.listing_id}"


class ActiveListings(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)


class Bids(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=99, default=None)
    bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date = models.DateTimeField(default=now,blank=True)
   

class Comments(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=99, default=None)
    comment = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=now,blank=True)


class Watchlist(models.Model):

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=99, default=None)
    date = models.DateTimeField(default=now,blank=True)


class Categories(models.Model):

    category = models.CharField(max_length=99, default=None)

    def __str__(self):
        return f"{self.category}" 
