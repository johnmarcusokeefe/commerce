from django import forms
from .models import Categories
from django.core.exceptions import ObjectDoesNotExist

import os

# create lists for select options:
CATEGORIES = []
FILE_LIST = []

# loads model data for catories. causes migration error when empty
cats = Categories.objects.values()
for cat in cats:
    temp = (cat.get('category').lower(), cat.get('category')) 
    CATEGORIES.append(temp)

#  uncomment data below when no model data available
# temp = ("empty","Empty")
# CATEGORIES.append(temp)

# set path for the base directory
path = "auctions/static/auctions/images"
dirs = os.listdir(path)
#print("dirs in forms", dirs)
# filter for file types to display in the dropdown
ext = [".jpg",".png"]
# add file list to select 
temp = ("default.png","Default")
FILE_LIST.append(temp)
for d in dirs:
    for e in ext:
        if d.find(e) != -1 and d != "default.png":
             temp = (d,d)
             FILE_LIST.append(temp)

# create listing form
class CreateListingForm(forms.Form): 
    title = forms.CharField(label="Enter Title", max_length=30)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    # category drop down
    category = forms.ChoiceField(choices = CATEGORIES)
    min_bid = forms.DecimalField(label="Starting bid $", min_value=0, decimal_places=0, initial=0)
    media_url = forms.ChoiceField(choices = FILE_LIST)

# bid form
class BidForm(forms.Form):
    
    bid = forms.DecimalField(label="",min_value=0, decimal_places=0, initial=0)
    


# comment form
class CommentForm(forms.Form):
    
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), label="")



