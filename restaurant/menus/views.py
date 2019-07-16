from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from menus.models import *
from menus.forms import *
from django.db import IntegrityError
from django.http import HttpResponseRedirect,HttpResponseNotAllowed
from django.urls import reverse
# Create your views here.

# Signup


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                print("---Creds given---")
                user.has_perm('menus.add_order')
                user.has_perm('menus.view_order')
                user.save()
            else:
                print("---Creds denied---")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# List Restaurants
def restaurantList(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'index.html', context={'res': restaurants})


# Create New Restaurant
# @login_required
@staff_member_required
def createRestaurant(request):
    form = RestaurantForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'createRestaurant.html', {'form': form})


# Updating a Restaurant
# @login_required
@staff_member_required
def updateRestaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'createRestaurant.html', {'form': form, 'restaurant': restaurant})


# Deleting a Restaurant
# @login_required
@staff_member_required
def deleteRestaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)

    if request.method == 'POST':
        restaurant.delete()
        return redirect('/')

    return render(request, 'deleteRestaurant.html', {'restaurant': restaurant})


# Listing all Items
def listItems(request, id):
    res = Restaurant.objects.get(id=id)
    items = Item.objects.filter(restaurant=id).all()
    return render(request, 'listItems.html', context={'items': items, 'res': res})


# Adding an Item
# @login_required
@staff_member_required
def addItem(request, id):
    restaurant = Restaurant.objects.get(id=id)
    form = ItemForm(request.POST or None, initial={'restaurant': id})

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'addItem.html', {'form': form})


# Updating an Item
# @login_required
@staff_member_required
def updateItem(request, res_id, item_id):
    restaurant = Restaurant.objects.get(id=res_id)
    item = Item.objects.get(id=item_id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'addItem.html', {'form': form, 'item': item, 'res': restaurant})


# Deleting an Item
# @login_required
@staff_member_required
def deleteItem(request, res_id, item_id):
    restaurant = Restaurant.objects.get(id=res_id)
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    return render(request, 'deleteItem.html', {'item': item})

# Add to cart
@login_required
def add_cart(request):
    if request.method == "POST":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity", "1"))
        item = Item.objects.get(pk=item_id)
        cart = Cart.objects.get_or_create(user=request.user, checked_out=False)
        qs = Order.objects.filter(Item=item, cart=cart[0])
        if qs:
            qs[0].quantity += quantity
            qs[0].save()
        else:
            ca = Order.objects.create(
                Item=item, quantity=quantity, cart=cart[0])

        return HttpResponseRedirect(reverse('listItems', args=(item.restaurant.pk,)))

# Checkout
@login_required
def check_out(request):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user,checked_out=False)
        cart.checked_out = True
        cart.save()
        return render(request, 'confirmed.html')
        
# Show cart
@login_required
def show_cart(request):
    try:
        cart = Cart.objects.get(user=request.user,checked_out=False)
    except Cart.DoesNotExist:
        return HttpResponseRedirect(reverse('main'))

    order = Order.objects.filter(cart=cart)
    return render(request, "show_cart.html", context={"items": order})

# Past orders
@login_required
def past_orders(request):
    cart = Cart.objects.filter(user=request.user,checked_out=True)
    return render(request, "past_orders.html", context={"carts": cart})


# Cart Items 
@login_required
def cart_items(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    if cart.user != request.user:
        return HttpResponseNotAllowed("this cart id doesn't belong to you")
    else:
        order = Order.objects.filter(cart=cart)
        return render(request, "show_cart_order.html", context={"items": order,'checked':cart.checked_out})
