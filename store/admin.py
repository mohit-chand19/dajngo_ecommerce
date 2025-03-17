from django.contrib import admin
from .models import Category,Customer,Product,Order,Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mix Profile info with User info
class ProfileInLine(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username","first_name","last_name","email"]
    inlines = [ProfileInLine]

# Unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)