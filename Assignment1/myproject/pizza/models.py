from django.db import models
from django.contrib.auth.models import User

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Crust(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Sauce(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Cheese(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=None)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE, default=None)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE, default=None)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE, default=None)
    
    pepperoni = models.BooleanField(default=False)
    chicken = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    pineapple = models.BooleanField(default=False)
    peppers = models.BooleanField(default=False)
    mushrooms = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)

    @property
    def toppings(self):
        selected_toppings = [name for name in ['pepperoni', 'chicken', 'ham', 'pineapple', 'peppers', 'mushrooms', 'onions'] if getattr(self, name)]
        if selected_toppings:
            if len(selected_toppings) > 1:
                return ', '.join(selected_toppings[:-1]).title() + ' and ' + selected_toppings[-1].title()
            return selected_toppings.title()
        return "No toppings"
    
    # String of the Pizza object
    def __str__(self):
        return f"{self.size} pizza with {self.crust} crust, {self.sauce} sauce, {self.cheese} cheese with {self.toppings.lower()}"
    
class Customer(models.Model):
    
    # Fields for customer details
    name = models.CharField(max_length=100, blank=False)
    house_number = models.CharField(max_length=10, blank=False)
    street = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=100, blank=False)
    card_number = models.CharField(max_length=16, blank=False)
    expiry_date = models.DateField(blank=False)
    cvv = models.CharField(max_length=4, blank=False)
    
    def address(self):
        return f"{self.house_number} {self.street}, {self.city}"
    
    # String of the Customer object
    def __str__(self):
        return f"Order by {self.name}, {self.address()}"

class Order(models.Model):
    
    # Foreign key to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign key to the Pizza model
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    # Fields for order details
    name = models.CharField(max_length=100)  # Add name field for order display
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    # String representation of the Order object
    def __str__(self):
        return f"Order by {self.name} on {self.order_date.strftime('%Y-%m-%d')}"