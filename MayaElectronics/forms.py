from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminFileWidget
from .models import Department, User, Order, Product, CartItem, Cart
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe



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

    product = forms.ModelChoiceField(queryset=Product.objects.all())


class CartForm(forms.Form):
    product_name = forms.CharField()  # This should match the type of 'id' field in your Product model
    quantity = forms.IntegerField()

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class ImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and getattr(value, "url", None):
            image_url = value.url
            output = (
                f'<a href="{image_url}" target="_blank"><img src="{image_url}" alt="{name}" style="max-height: 200px; max-width: 200px;" /></a>'
            )
        return mark_safe(output)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'quantity', 'available', 'category', 'image']

    image = forms.ImageField(label='Product Image', required=False, widget=ImageWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
