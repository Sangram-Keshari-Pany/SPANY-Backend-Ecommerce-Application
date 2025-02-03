from django.contrib import admin
from SPANYAPP.models import ShippingAddress
from SPANYAPP.models import Category,SubCategory,Product,FlashSale,Favorites
from SPANYAPP.models import Order,OrderItems,Review
from SPANYAPP.models import CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ShippingAddress)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(FlashSale)

admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Favorites)

admin.site.register(Review)


