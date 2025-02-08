from rest_framework import serializers
from SPANYAPP.models import CustomUser, Category, SubCategory, Product, FlashSale
from SPANYAPP.models import Order, OrderItems, Favorites, Review
from django.contrib.auth.models import User

# ------------------- USER SERIALIZERS -------------------
# USER SERIALIZER 
class RegistationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'], password=validated_data['password'], email=validated_data['email'])
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user', 'phone_number', 'profile_picture']


class CustomerFetch(serializers.ModelSerializer):
    user = RegistationSerializer()

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)  # Create the User instance first
        customuser = CustomUser(user=user, **validated_data)  # Pass the rest of the data to create CustomUser
        customuser.save()
        return customuser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

# ------------------- PRODUCT AND CATEGORY SERIALIZERS -------------------
# CATEGORY SERIALIZER 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# SUBCATEGORY SERIALIZER 
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


# PRODUCT SERIALIZER 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# ------------------- FLASH SALE SERIALIZER -------------------
# FLASH SALE SERIALIZER 
class FlashSaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = FlashSale
        fields = ['id', 'start_time', 'end_time', 'quantity_in_stock', 'discount_percentage', 'product']

# ------------------- ORDER AND ORDER ITEMS SERIALIZERS -------------------
# ORDER SERIALIZER 
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


# ORDER ITEMS SERIALIZER 
class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


# CART ITEMS SERIALIZER 
class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()

    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'order', 'quantity', 'date_added']

# ------------------- FAVORITES SERIALIZER -------------------
# FAVORITES SERIALIZER 
class FavoritesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Favorites
        fields = ['id', 'product']

# ------------------- REVIEW SERIALIZER -------------------
# REVIEW SERIALIZER 
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
