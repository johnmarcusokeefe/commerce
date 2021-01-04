from django import forms
from .models import Categories


# create a list of tuples for the select functionality
tc = Categories.objects.values()
TEST_CHOICES = []
for t in tc:
    temp = (t.get('category').lower(),t.get('category')) 
    TEST_CHOICES.append(temp)


class ListingForm(forms.Form): 
    title = forms.CharField(label="Enter Title", max_length=30)
    description = forms.CharField(label = "Enter Description", max_length=100)
    # category drop down
    category = forms.CharField(widget = forms.Select(choices = TEST_CHOICES))
    min_bid = forms.DecimalField(label = "Minimum Bid")
    media_url = forms.CharField(label = "Media URL", max_length=30)
