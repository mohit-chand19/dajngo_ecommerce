from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_order"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_order","shipped","date_shipped"]
    inlines = [OderItemInline]

# Unregister Order Model
admin.site.unregister(Order)
# Re-register Order Model and OrderAdmin model(which now holds orderitem stuff)
admin.site.register(Order, OrderAdmin)