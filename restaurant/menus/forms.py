from django import forms
from menus.views import *


# Creating a new Restaurant
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine']



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item

        fields = ['name', 'description', 'price', 'restaurant']