from store.models import Product, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the user
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session_key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        
        # Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'1':3, '3':5}[this is dictionary] to {"1":3, "3":5} [this is JSON format]
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save the carty to the user Profile
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'1':3, '3':5}[this is dictionary] to {"1":3, "3":5} [this is JSON format]
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save the carty to the user Profile
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get Ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get Cart
        our_cart = self.cart

        # update our cart(which is dictionary)
        our_cart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'1':3, '3':5}[this is dictionary] to {"1":3, "3":5} [this is JSON format]
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save the carty to the user Profile
            current_user.update(old_cart=str(carty))

        updated_cart = self.cart
        return updated_cart
    
    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'1':3, '3':5}[this is dictionary] to {"1":3, "3":5} [this is JSON format]
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save the carty to the user Profile
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # Get product ids
        product_ids = self.cart.keys()
        # lookup for those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # start quantities at 0
        total = 0
        for key, value in quantities.items(): #quantities are like dictionaries {'id' : quantity}
            # convert key string into int to do calculation
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total