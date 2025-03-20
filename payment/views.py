from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from django.contrib import messages
from .models import ShippingAddress
from store.models import Profile

# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html",{})

def shipping_info(request):
    if request.user.is_authenticated:        
        # Get the current user Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if shipping_form.is_valid():
            shipping_form.save()

            messages.success(request, "Your Info Has Been Updated...")
            return redirect('home')
        return render(request, "payment/shipping_info.html", {'shipping_form':shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('home')
    

def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:     
        # Checkout for logged in user

        # get the current shipping user info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

           
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

    else:
        # Checkout for the guest user
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, 'quantities':quantities, 'totals':totals,'shipping_form':shipping_form})
    
def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Check to see if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products, 'quantities':quantities, 'totals':totals,'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products":cart_products, 'quantities':quantities, 'totals':totals,'shipping_info':request.POST, 'billing_form':billing_form})

    else:
        messages.success(request, "Access Denied!")
        return redirect('home')
