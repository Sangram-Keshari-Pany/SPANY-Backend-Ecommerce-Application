from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from SPANYAPP.models import CustomUser
from SPANYAPP.models import Category,SubCategory,Product,FlashSale
from SPANYAPP.models import Order,OrderItems,Favorites,Review
from SPANYAPP.serializer import CategorySerializer,SubCategorySerializer,ProductSerializer,FlashShaleSerializer
from SPANYAPP.serializer import OrderItemsSerializer,CartitemsSerializer,FavoritesSerializer,ReviewSerializer,OrderSerializer
from django.utils import timezone
from rest_framework import status

from SPANYAPP.serializer import RegistationSerializer,CustomUserSerializer,LoginSerializer,CustomerFetch
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import  permissions
# Create your views here.

############             #############
############   USER API  #############
############             #############
class RegistrationView(GenericAPIView):
    serializer_class=RegistationSerializer
    def post(self,request,*args,**kwargs):
        validate_data=request.data
        userdata=validate_data.pop('user')
        print(userdata,"user----->")
        print(validate_data,'validatedata')

        user_serializer=self.get_serializer(data=userdata)
        user_serializer.is_valid(raise_exception=True)
        user=user_serializer.save()
        print(validate_data,'validatedata')
        validate_data['user']=user.id
        custom_user_serializer=CustomUserSerializer(data=validate_data)
        custom_user_serializer.is_valid(raise_exception=True)
        custom_user=custom_user_serializer.save()

        refresh=RefreshToken.for_user(user)

        return Response(
            {
            'user':RegistationSerializer(user,context=self.get_serializer_context()).data,
            'custom_user':CustomUserSerializer(custom_user,context=CustomUserSerializer).data,
            'refresh':str(refresh),
            'access':str(refresh.access_token)
            }
        )

class CustomerFetchView(ListAPIView):
    serializer_class=CustomerFetch
    def get_queryset(self):
        username = self.kwargs.get('username')
        custom_user=CustomUser.objects.filter(user__username=username)
        return custom_user

class LoginView(GenericAPIView):
    serializer_class=LoginSerializer
    def post (self,request,*args,**kwargs):
        username=request.data['username']
        password=request.data['password']
        
        user=authenticate(username=username,password=password)
        custom_user=CustomUser.objects.get(user=user)
        print(custom_user)
        if user is not None:
            refresh=RefreshToken.for_user(user)
        
            return Response({
                'user':RegistationSerializer(user,context=self.get_serializer_context()).data,
                'custom_user':CustomUserSerializer(custom_user,many=False).data,
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            })

class FavoritesView(ListAPIView):
    serializer_class=FavoritesSerializer
    def get_queryset(self):
        favorites=Favorites.objects.filter(user=self.request.user)
        return favorites

class ReviewView(ListAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

############             #############
############ PRODUCT API #############
############             #############
class CategoryView (ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated] 
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class SubCategoryView(ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated] 
    queryset=SubCategory.objects.all()
    serializer_class=SubCategorySerializer

class ProductView(ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated] 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class FlashShaleView(ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated] 
    queryset=FlashSale.objects.filter(end_time__gt=timezone.now())
    serializer_class=FlashShaleSerializer

############             #############
############ ORDER API   #############
############             #############

class CartItemsView(ListAPIView):
    serializer_class=CartitemsSerializer
    def get_queryset(self):
        orderitems = OrderItems.objects.filter(order__user=self.request.user, order__complete=False)
        return orderitems

class OrderView(UpdateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    lookup_field="id"

class DeliverItemsView(APIView):
    def get (self,request,*args,**kwargs):
        orders = Order.objects.filter(user=request.user,complete=True)
        order_serializer=OrderSerializer(orders,many=True).data
        order_arraay = []
        for order in order_serializer:
            order_items = OrderItems.objects.filter(order=order['id'])
            order_items_serializer=CartitemsSerializer(order_items,many=True).data
            order_arraay.append(order_items_serializer)

        return Response(order_arraay)

class OrderItemsView(APIView):
    def post (self,request,*args,**kwargs):
        order,created=Order.objects.get_or_create(user=request.user,complete=False)
        orderitemdata=request.data
        orderitemdata.update({'order':order.id,'user':request.user})
        functionality=orderitemdata.pop('functionality')
        try :
            orderitem=OrderItems.objects.get(product=orderitemdata['product'],order=orderitemdata['order'])
            if functionality=="add":
                orderitem.quantity+=1
            elif functionality=="remove":
                orderitem.quantity-=1
            orderitem.save()
            if orderitem.quantity<=0:
                orderitem.delete()
            print("try")
            return Response({"success": "quantyty added successfully"}, status=status.HTTP_201_CREATED)
        except:
            orderItemsoerializer=OrderItemsSerializer(data=orderitemdata)
            if orderItemsoerializer.is_valid():
                orderItemsoerializer.save()
                return Response({"success": "Added successfully"}, status=status.HTTP_201_CREATED)
            return Response({"error": "Error in the data", "details": orderItemsoerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def example (request):
    user=User.objects.all()
    user.delete()
    return Response ({'sycess':"sucess"})