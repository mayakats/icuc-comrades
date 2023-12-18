from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Department, User, Order, Product, CartItem, Cart

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']

    DEPARTMENT_NAME_OPTIONS = [
        ("IT", "Information Technology"),
        ("F", "Finance"),
        ("M", "Maintenance"),
        ("P", "Production"),
    ]

    department_name = forms.ChoiceField(choices=DEPARTMENT_NAME_OPTIONS)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class CartForm(forms.Form):
    product_name = forms.CharField()  # This should match the type of 'id' field in your Product model
    quantity = forms.IntegerField()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'quantity', 'available']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product_item', 'amount']
