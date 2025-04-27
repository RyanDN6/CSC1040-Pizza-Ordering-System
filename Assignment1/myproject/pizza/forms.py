from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import *

# Form for user sign-up, extending Django's UserCreationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Form for creating or updating a Pizza instance
class PizzaForm(forms.ModelForm):

    size = forms.ModelChoiceField(queryset=Size.objects.all())
    crust = forms.ModelChoiceField(queryset=Crust.objects.all())
    sauce = forms.ModelChoiceField(queryset=Sauce.objects.all())
    cheese = forms.ModelChoiceField(queryset=Cheese.objects.all())

    # Optional boolean fields for pizza toppings
    pepperoni = forms.BooleanField(required=False)
    chicken = forms.BooleanField(required=False)
    ham = forms.BooleanField(required=False)
    pineapple = forms.BooleanField(required=False)
    peppers = forms.BooleanField(required=False)
    mushrooms = forms.BooleanField(required=False)
    onions = forms.BooleanField(required=False)

    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'pepperoni', 'chicken', 'ham', 'pineapple', 'peppers', 'mushrooms', 'onions']

# Form for creating or updating a Customer instance
class CustomerForm(forms.ModelForm):

    # Fields for credit card information with specific widgets and validation
    card_number = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Card Number'}), max_length=16, required=True)
    cvv = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'CVV'}), max_length=4, required=True)
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Customer
        fields = ['name', 'house_number', 'street', 'city', 'card_number', 'expiry_date', 'cvv']

    # Custom validation for card number
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValidationError("Credit card number invalid format.")
        return card_number

    # Custom validation for CVV
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit() or not (3 <= len(cvv) <= 4):
            raise ValidationError("CVV invalid format.")
        return cvv

    # Custom validation for expiry date
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date <= date.today():
            raise ValidationError("This card has expired.")
        return expiry_date
