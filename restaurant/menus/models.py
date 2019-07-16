from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    cuisine = models.CharField(max_length = 50)
    class Meta:
        verbose_name = ("Restaurant")
        verbose_name_plural = ("Restaurants")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("Item")
        verbose_name_plural = ("Items")

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Model definition for Cart."""
    checked_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    Items = models.ManyToManyField('Item',through='Order')
    # TODO: Define fields here
    @property
    def total(self):
        total = 0
        for item in Order.objects.filter(cart=self):
            total+= item.Item.price*item.quantity
        return total
    class Meta:
        """Meta definition for Cart."""

        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        """Unicode representation of Cart."""
        return str(self.user.pk)

class Order(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart', on_delete=models.CASCADE)
    Item = models.ForeignKey('Item',related_name='item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return str(self.cart.user.pk)
