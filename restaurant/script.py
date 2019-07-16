from menus.models import *

restaurant_array = {"Willys":'Burger', "Porta Doro":'Italian'}

for i in restaurant_array:
    new=Restaurant(name=i, cuisine = restaurant_array[i])
    new.save()