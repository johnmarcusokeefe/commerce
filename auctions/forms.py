from django import forms
from .models import Categories

import os

# create a list of tuples for the select functionality
tc = Categories.objects.values()

TEST_CHOICES = []
FILE_LIST = []

for t in tc:
    temp = (t.get('category').lower(), t.get('category')) 
    TEST_CHOICES.append(temp)

# set path for the base directory
path = "auctions/static/auctions/images"
dirs = os.listdir(path)
print("dirs in forms", dirs)
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


class CreateListingForm(forms.Form): 
    title = forms.CharField(label="Enter Title", max_length=30)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    # category drop down
    category = forms.ChoiceField(choices = TEST_CHOICES)
    min_bid = forms.DecimalField(label="Min Bid$", min_value=0, decimal_places=0, initial=0)
    media_url = forms.ChoiceField(choices = FILE_LIST)


class BidForm(forms.Form):
    # input
    bid = forms.DecimalField(label="",min_value=0, decimal_places=0, initial=0)
    

class CommentForm(forms.Form):
    
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), label="")



