from rest_framework import serializers
from .models import Department, User, Cart, CartItem, Category, Product, ProductImages, Feedback
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CartSerializers(serializers.ModelSerializer):
    """Get Cart list"""

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items',)


class CartItemSerializers(serializers.ModelSerializer):
    """Get CartItem List"""

    class Meta:
        model = CartItem
        fields = ('amount', 'product_item',)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        created_product = Product.objects.create(**validated_data)

        images_obj = [
            ProductImages(product=created_product, image=image) for image in images_data.getlist('image')
        ]
        ProductImages.objects.bulk_create(images_obj)
        return created_product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation

class ProductFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['feedbacks'] = FeedbackSerializer(instance.feedbacks.all(), many=True, context=self.context).data
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)  
        
        if instance.children.exists():
         
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class RegisterApiSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError("Password and Password2 did not match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(TokenObtainPairSerializer):
   
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password', None)
        
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
       
        user = authenticate(username=email, password=password)
        
        if user and user.is_active:
            refresh = self.get_token(user)
            
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'likes', 'dislikes') 

class FeedbackSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Feedback
        fields = ('id', 'body', 'author', 'product')