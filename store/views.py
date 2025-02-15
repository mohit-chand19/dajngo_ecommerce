from django.shortcuts import redirect, render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm



# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # authenticating the user
        if user is not None: # Checking if authentication was successful
            login(request, user)
            messages.success(request, "You have been logged in successfully!")
            return redirect('home')
        else:
            messages.success(request, "Wrong credentials...Try Again!")
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...Thanks for shopping with us!")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been Registered successfully! Welcome...")
            return redirect('home')
        else:
            print(form.errors)
            messages.success(request, "Whoops! There was an error while registering Try Again...")
            return redirect('register')      
        
    else:    
        return render(request, 'register.html', {'form':form})
    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})

def category(request, cat):
    # replacing hypens with spaces
    cat = cat.replace('-',' ')
    # Grab the category from url
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(Category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, "That category doesn't exist")
        return redirect('home')