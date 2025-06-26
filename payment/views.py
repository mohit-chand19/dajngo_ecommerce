from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from django.contrib import messages
from .models import ShippingAddress, Order, OrderItem
from store.models import Profile, Product
from django.contrib.auth.models import User


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "payment/not_shipped_dash.html",{'orders':orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "payment/shipped_dash.html",{'orders':orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


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

        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

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
    

def process_order(request):
    if request.POST:
        # Get the cart 
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        # Get the billing info from our last page
        payment_form = PaymentForm(request.POST or None)
        # Get the shipping session data
        my_shipping = request.session.get('my_shipping')
        # Gather Order Info
        full_name = my_shipping['full_name']
        email = my_shipping['email']
        # create shipping address from session info
        shipping_address = f"{my_shipping['address1']}\n{my_shipping['address2']}\n{my_shipping['city']}\n{my_shipping['province']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"
        amaount_paid = totals

        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amaount_paid)
            create_order.save()

            # add order items
            # get the order id
            order_id = create_order.pk

            # get the product info
            for product in cart_products:
                # get the product id
                product_id = product.id
                # get the product price
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                # get product quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # create an order
                        create_order_item = OrderItem(order_id=order_id ,product_id=product_id,user=user,quantity=value,price=product_price)
                        create_order_item.save() 
            
            # Delete our cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]


            messages.success(request, "Order Placed!")
            return redirect('home')
        
        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=totals)
            create_order.save()

            # add order items
            # get the order id
            order_id = create_order.pk

            # get the product info
            for product in cart_products:
                # get the product id
                product_id = product.id
                # get the product price
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                # get product quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # create an order
                        create_order_item = OrderItem(order_id=order_id ,product_id=product_id,quantity=value,price=product_price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]           

            messages.success(request, "Order Placed!")
            return redirect('home')
        
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')