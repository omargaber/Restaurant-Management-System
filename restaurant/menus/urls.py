from django.urls import path
from menus.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path('', restaurantList,name='main'),
    path('login/', auth_views.LoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('signup/', signup, name='signup'),
    path('newRestaurant/', createRestaurant, name='createRestaurant'),
    path('updateRestaurant/<int:id>', updateRestaurant, name='updateRestaurant'),
    path('deleteRestaurant/<int:id>', deleteRestaurant, name='deleteRestaurant'),
    path('restaurant/<int:id>/', listItems, name='listItems'),
    path('restaurant/<int:id>/addItem', addItem, name='addItem'),
    path('restaurant/<int:res_id>/<int:item_id>/edit', updateItem, name='updateItem'),
    path('restaurant/<int:res_id>/<int:item_id>/delete', deleteItem, name='deleteItem'),
    path('restaurant/cart/add',add_cart,name="add_cart"),
    path('restaurant/cart',show_cart,name='show_cart'),
    path('checkout', check_out, name='check_out'),
    path('pastOrders', past_orders, name='past_orders'),
    path('cartItems/<int:cart_id>', cart_items, name='cart_items'),
    path('confirmed/', check_out, name='check_out')
]
