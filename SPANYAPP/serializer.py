from rest_framework import serializers
from SPANYAPP.models import CustomUser
from SPANYAPP.models import Category,SubCategory,Product,FlashSale
from SPANYAPP.models import Order,OrderItems,Favorites,Review
from django.contrib.auth.models import User


class RegistationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
    
    def create (self,validate_data):
        user=User(username=validate_data['username'],password=validate_data['password'],email=validate_data['email'])
        user.set_password(validate_data['password'])
        user.save()
        return user 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['user','phone_number','profile_picture']


class CustomerFetch(serializers.ModelSerializer):
    user=RegistationSerializer()
    class Meta:
        model=CustomUser
        fields="__all__"

    def create (self,validate_data):
        customuser=CustomUser(user=validate_data['user'],phone_number=validate_data['phone_number'],profile_picture=validate_data['profile_picture'])
        customuser.save()
        return customuser

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields="__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class FlashShaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=FlashSale
        fields= ['id', 'start_time', 'end_time','quantity_in_stock','discount_percentage', 'product']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItems
        fields="__all__"

class CartitemsSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    order=OrderSerializer()
    class Meta:
        model=OrderItems
        fields=['id','product','order','quantity','date_added']

class FavoritesSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=Favorites
        fields=['id','product']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"
