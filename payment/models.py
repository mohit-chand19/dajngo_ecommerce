from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)

    # Dont pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'{self.user.username}\'s Shipping Address'
    
    
# create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user = instance)
        user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)

# Create Order Model
class Order(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order - {str(self.id)}"

# Create Order Items Model
class OrderItem(models.Model):
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Order Items"