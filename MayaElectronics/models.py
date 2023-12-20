from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils import timezone 
import datetime

User = get_user_model()

class Department(models.Model):
    DEPARTMENT_NAME_OPTIONS = [
        ("IT", "Information Technology"),
        ("F", "Finance"),
        ("M", "Maintenance"),
        ("P", "Production"),
    ]

    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, choices=DEPARTMENT_NAME_OPTIONS)

    class Meta:
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.department_name

class User(models.Model):
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    user_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    salutation = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    gender = models.CharField(max_length=2, choices=GENDER_OPTIONS)
    username = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dob = models.DateField()
    marital_status = models.CharField(max_length=255)
    job_role = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.fullname

class Category(models.Model):
    name = models.CharField(max_length=150, default='SOME STRING')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children', blank=True)

    def __str__(self):
        if not self.parent:
            return f'{self.name}'
        else:
            return f'{self.parent} --> {self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price =models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255, default=None)
    description = RichTextField()
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    def __str__(self):
        return self.title

 
class ProductImages(models.Model):
    image = models.ImageField(upload_to='products', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    
    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
class CartManger(models.Manager):
    def get_or_new(self, request):
        user = request.user 
        cart_id = request.session.get('cart_id', None)
        if user is not None and user.is_authenticated:
            try:
                if user.cart:
                    cart_obj = request.user.cart 

                else:
                    cart_obj = Cart.objects.get(pk=cart_id)
                    cart_obj.user = user
                    cart_obj.save()  
                return cart_obj
            except:
                 HttpResponse("")
        else:
            cart_obj = Cart.objects.get_or_create(pk=cart_id)
            cart_id = request.session['cart_id'] = cart_obj[0].id
            return cart_obj[0]

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    objects = CartManger()

    def __str__(self):
        if self.user:
            return f"cart for {self.user}"
        else:
            return "anonymous cart"
        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    amount = models.PositiveIntegerField(default=1, blank=True)
    
    def __str__(self):
        return f"{self.cart.id} == cart item"

 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.product.name if self.product else 'N/A'}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    activation_code = models.CharField(max_length=40, blank=True)
    objects = CustomUserManager()
    email = models.EmailField('Email address', unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception('Code is invalid')
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])
class Feedback(models.Model):
    author = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='feedbacks', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}-->{self.product}-->{self.created_at}-{self.body[0:10]}"
