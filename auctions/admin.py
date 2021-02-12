from django.contrib import admin
from .models import Categories, Listings, Watchlist, Comments, Bids

# Register your models here.
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)
