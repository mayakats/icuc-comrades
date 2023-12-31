from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from MayaElectronics.forms import UserForm, OrderForm, CartItemForm, ProductForm
from MayaElectronics.models import Department, User, Product, ProductImages, Order, Cart, CartItem, Category, Feedback
from rest_framework import viewsets, generics, permissions, serializers, status
from .serializers import UserSerializer, CartItemSerializers, CartSerializers, ProductImageSerializer, CategorySerializer, LikeSerializers, ProductFeedbackSerializer,FeedbackSerializer, RegisterApiSerializer, LoginSerializer
from rest_framework.pagination import PageNumberPagination
from . import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from MayaElectronics.send_mail import send_confirmation_email
from MayaElectronics.permissions import IsOwnerOrReadOnly
from django.http import HttpResponse
from django.db import IntegrityError
import uuid 
from django.http import Http404

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index_page')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index_page')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def index_view(request):
    return render(request, 'index.html')

def products_view(request):
    return render(request,'products.html')

def aboutus_view(request):
    return render(request,'aboutus.html')

def gallery_view(request):
    return render(request,'gallery.html')

def contactus_view(request):
    return render(request,'contactus.html')

def update_user_view(request, user_id):
    user = User.objects.get(pk=user_id)
    message = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            message = "User updated Successfully"

    else:
        user_form = UserForm(instance=user)

    context = {
        'form': user_form,
        'user': user,
        'msg': message
    }

    return render(request, 'update_user.html', context)
def edit_user_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")  # or redirect to a custom error page
    message = ''

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            message = "Changes saved Successfully"
        else:
            message = "Form has Invalid data"
    else:
        user_form = UserForm(instance=user)

    context = {
        'form': user_form,
        'user': user,
        'message': message
    }

    return render(request, 'edit_user.html', context)
def delete_user_view(request, user_id):
    user = User.objects.get(id=user_id)  # Use 'id' instead of 'user_id'
    user.delete()
    return redirect('display_data_view')

def order_page(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success') 
    else:
        form = OrderForm()

    products = Product.objects.all()
    return render(request, 'order_page.html', {'form': form, 'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product.id)
    else:
        form = ProductForm()

    categories = Category.objects.all()
    context = {'categories': categories, 'form': form}
    return render(request, 'add_product.html', context)

def products_list_view(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})
    
class CartItemView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assuming you have a way to associate the cart item with a user
        serializer.save(user=self.request.user)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers
    permission_classes = [IsAuthenticated]

def perform_create(self, serializer):
        cart = Cart.objects.get_or_new(self.request)
        serializer.save(cart=cart)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination 

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)

class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)

class ProductImageView(generics.ListAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser,)

class ProductFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
                Q(title__icontains=query) | Q(price__icontains=query)
            )
        return object_list

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FeedbackListCreateView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedbackDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # Replace 'Product' with the actual model name
    serializer_class = ProductFeedbackSerializer  # Replace with the correct serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

def add_to_cart(request):
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('product_list')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')

def cart_view(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart_view.html', {'cart_items': cart_items, 'total_price': total_price})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)