from django.shortcuts import redirect, render
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q



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
            messages.success(request, "You have been Registered successfully! Please Fill Out User Details...")
            return redirect('update_info')
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
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated...")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('home')
    

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            # Check if the form is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated Successfully...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.success(request, error)

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
        
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated...")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('home')
    

def search(request):
    # Determine if they fill out the form
    if request.method == "POST":
        searched = request.POST["searched"]
        products = Product.objects.filter(
            Q(name__icontains=searched) | Q(Category__name__icontains=searched) | Q(description__icontains=searched)
        )
        if not products:
            messages.success(request, "Sorry that product does not found...Try Again!")
            return redirect('search')

        else:
            return render(request, "search.html", {'searched':searched, 'products':products})

    else:
        return render(request, "search.html", {})