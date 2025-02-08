from django.urls import path
from SPANYAPP.views import (
    RegistrationView, LoginView, CustomerFetchView,
    CategoryView, SubCategoryView, ProductView, FlashShaleView,
    OrderItemsView, CartItemsView, DeliverItemsView, FavoritesView, 
    ReviewView, OrderView,
    )

urlpatterns = [
    # User Authentication Routes
    path("registration/", RegistrationView.as_view(), name="user-registration"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("customerfetch/<str:username>/", CustomerFetchView.as_view(), name="fetch-customer"),

    # Product Routes
    path("category/", CategoryView.as_view(), name="product-category"),
    path("sub_category/", SubCategoryView.as_view(), name="product-subcategory"),
    path("product/", ProductView.as_view(), name="product-list"),
    path("flashshale/", FlashShaleView.as_view(), name="flash-sale-list"),

    # Cart and Order Routes
    path("cartitems/", CartItemsView.as_view(), name="cart-items"),
    path("deliveritems/", DeliverItemsView.as_view(), name="delivered-items"),
    path("orderitems/", OrderItemsView.as_view(), name="order-items"),
    path("orderview/<int:id>/", OrderView.as_view(), name="order-detail"),

    # Favorites and Reviews
    path("favorites/", FavoritesView.as_view(), name="user-favorites"),
    path("review/", ReviewView.as_view(), name="product-reviews"),

    # Example Endpoint (Consider removing or securing this endpoint)
]
