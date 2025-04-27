from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreationForm, PizzaForm, CustomerForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Pizza, Order

# View for user signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect("home")  # Redirect to homepage after signup
    else:
        form = UserCreationForm()
    
    return render(request, "signup.html", {"form": form})

# View for the homepage
def home(request):
    
    # Get the logged-in user and their previous orders
    if request.user.is_authenticated:
        previous_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    else:
        previous_orders = []

    return render(request, 'home.html', {'previous_orders': previous_orders})

# View to render the order page
def make_order(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            return render(request, 'review.html', {'pizza':pizza})  # Render review page with pizza details
        else:
            return render(request, 'order.html', {'form':form})  # Re-render order page with form errors
    else:
        form = PizzaForm()
        return render(request, 'order.html', {'form':form})  # Render order page with empty form

# View for user login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in after successful authentication
                return redirect("home")  # Redirect to home page after login
            else:
                form.add_error(None, "Invalid username or password")  # Add error if authentication fails
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

# View for user logout
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage after logout

# View for handling delivery details
def delivery(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()

            # Get the latest pizza order
            pizza = Pizza.objects.latest('id')  

            # Create the order
            Order.objects.create(
                user=request.user,  # Link to the current logged-in user
                pizza=pizza,  # Link to the latest pizza order
                address=customer.address(),  # Save the formatted address
                name=customer.name
            )

            # Redirect to order success page, passing pizza and customer info
            return render(request, 'order_success.html', {'customer': customer, 'pizza': pizza})
    
    else:
        form = CustomerForm()

    return render(request, 'delivery.html', {'form': form})  # Render delivery page with form
