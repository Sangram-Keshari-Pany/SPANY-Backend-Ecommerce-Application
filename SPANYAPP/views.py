from rest_framework.generics import ListAPIView,  UpdateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from SPANYAPP.models import CustomUser, Category, SubCategory, Product, FlashSale, Order, OrderItems, Favorites, Review
from SPANYAPP.serializer import CategorySerializer, SubCategorySerializer, ProductSerializer, FlashSaleSerializer
from SPANYAPP.serializer import OrderItemsSerializer, CartItemsSerializer, FavoritesSerializer, ReviewSerializer, OrderSerializer
from django.utils import timezone
from rest_framework import status
from SPANYAPP.serializer import RegistationSerializer, CustomUserSerializer, LoginSerializer, CustomerFetch
from rest_framework.permissions import  IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# ##########################
# USER API VIEWS
# ##########################

class RegistrationView(GenericAPIView):
    """
    User registration API.
    Creates a new user and custom user profile.
    Returns access and refresh tokens.
    """
    serializer_class = RegistationSerializer

    def post(self, request, *args, **kwargs):
        validated_data = request.data
        userdata = validated_data.pop('user')

        # Serialize and save user data
        user_serializer = self.get_serializer(data=userdata)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        validated_data['user'] = user.id
        custom_user_serializer = CustomUserSerializer(data=validated_data)
        custom_user_serializer.is_valid(raise_exception=True)
        custom_user = custom_user_serializer.save()

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': RegistationSerializer(user, context=self.get_serializer_context()).data,
            'custom_user': CustomUserSerializer(custom_user, context=CustomUserSerializer).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class CustomerFetchView(ListAPIView):
    """
    Fetch customer details using username.
    """
    serializer_class = CustomerFetch

    def get_queryset(self):
        username = self.kwargs.get('username')
        return CustomUser.objects.filter(user__username=username)

class LoginView(GenericAPIView):
    """
    Login API for users.
    Returns JWT tokens if authentication is successful.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            custom_user = CustomUser.objects.get(user=user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': RegistationSerializer(user, context=self.get_serializer_context()).data,
                'custom_user': CustomUserSerializer(custom_user, many=False).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class FavoritesView(ListAPIView):
    """
    API to get all favorite products of the authenticated user.
    """
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

class ReviewView(ListAPIView):
    """
    API to get all reviews of products.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# ##########################
# PRODUCT API VIEWS
# ##########################

class CategoryView(ListAPIView):
    """
    Fetch all product categories.
    Requires authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryView(ListAPIView):
    """
    Fetch all product subcategories.
    Requires authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ProductView(ListAPIView):
    """
    Fetch all products.
    Requires authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class FlashShaleView(ListAPIView):
    """
    Fetch products that are on flash sale (active).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FlashSale.objects.filter(end_time__gt=timezone.now())
    serializer_class = FlashSaleSerializer


# ##########################
# ORDER API VIEWS
# ##########################

class CartItemsView(ListAPIView):
    """
    Fetch cart items for the authenticated user.
    """
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        return OrderItems.objects.filter(order__user=self.request.user, order__complete=False)

class OrderView(UpdateAPIView):
    """
    Update an existing order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

class DeliverItemsView(APIView):
    """
    Fetch completed orders and their items for the authenticated user.
    """
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, complete=True)
        order_serializer = OrderSerializer(orders, many=True).data

        order_array = []
        for order in order_serializer:
            order_items = OrderItems.objects.filter(order=order['id'])
            order_items_serializer = CartItemsSerializer(order_items, many=True).data
            order_array.append(order_items_serializer)

        return Response(order_array)

class OrderItemsView(APIView):
    """
    Add or remove items from the order.
    If the product is already in the order, update the quantity.
    """
    def post(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderitemdata = request.data
        orderitemdata.update({'order': order.id, 'user': request.user})
        functionality = orderitemdata.get('functionality', None)  # Safer retrieval of functionality

        try:
            # Check if the item exists in the order
            orderitem = OrderItems.objects.get(product=orderitemdata['product'], order=orderitemdata['order'])
            if functionality == "add":
                orderitem.quantity += 1
            elif functionality == "remove":
                orderitem.quantity -= 1
            orderitem.save()

            # Delete item if quantity is 0 or less
            if orderitem.quantity <= 0:
                orderitem.delete()

            return Response({"success": "Quantity updated successfully"}, status=status.HTTP_200_OK)

        except OrderItems.DoesNotExist:
            # Create new order item if it doesn't exist
            order_item_serializer = OrderItemsSerializer(data=orderitemdata)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
                return Response({"success": "Added successfully"}, status=status.HTTP_201_CREATED)

            return Response({"error": "Error in the data", "details": order_item_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



