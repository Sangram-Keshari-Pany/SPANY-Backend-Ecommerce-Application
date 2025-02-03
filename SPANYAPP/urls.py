from django.urls import path
from SPANYAPP.views import RegistrationView,LoginView,CustomerFetchView
from SPANYAPP.views import CategoryView,SubCategoryView,ProductView,FlashShaleView
from SPANYAPP.views import OrderItemsView,CartItemsView,DeliverItemsView,FavoritesView,ReviewView,OrderView,example
urlpatterns=[
    path("registration",RegistrationView.as_view()),
    path("login",LoginView.as_view()),
    path("customerfetch/<str:username>",CustomerFetchView.as_view()),
    path("category",CategoryView.as_view()),
    path("sub_category",SubCategoryView.as_view()),
    path("product",ProductView.as_view()),
    path("flashshale",FlashShaleView.as_view()),
    path("cartitems",CartItemsView.as_view()),
    path("deliveritems",DeliverItemsView.as_view()),
    path("orderitems",OrderItemsView.as_view()),
    path("favorites",FavoritesView.as_view()),
    path("review",ReviewView.as_view()),
    path("orderview/<int:id>",OrderView.as_view()),
    path("example",example)
]