from django.db import models
# Create your models here.
from django.contrib.auth.models import User

##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########
##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########
##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########------USER MODELS--------##########
class CustomUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username




###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########
###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########
###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########------PRODUCT MODELS--------###########
class Category (models.Model):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to="Category",blank=True,null=True)

    def __str__(self):
        return self.category_name
    
class SubCategory (models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    sub_category_name=models.CharField(max_length=100)
    sub_category_image=models.ImageField(upload_to="SubCategory",blank=True,null=True)

    def __str__(self):
        return self.category.category_name+"--->"+self.sub_category_name

class Product (models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.SET_NULL,blank=True,null=True)
    product_name=models.CharField(max_length=500)
    product_image1=models.ImageField(upload_to="Product",blank=True,null=True)
    product_image2=models.ImageField(upload_to="Product",blank=True,null=True)
    product_image3=models.ImageField(upload_to="Product",blank=True,null=True)
    product_image4=models.ImageField(upload_to="Product",blank=True,null=True)
    product_image5=models.ImageField(upload_to="Product",blank=True,null=True)
    Highlights=models.TextField(blank=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.DecimalField(max_digits=10,decimal_places=2)
    cost_price=models.DecimalField(max_digits=10,decimal_places=2)
    minimum_order_quantity=models.PositiveIntegerField()
    size=models.CharField(max_length=255)
    color=models.CharField(max_length=255)
    material=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    specification=models.TextField()
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    keyword=models.TextField()
    warenty=models.TextField()
    like=models.BigIntegerField(default=0)

    def __str__(self):
        return self.product_name

class FlashSale(models.Model):
    product = models.ForeignKey(Product, related_name="flash_sales", on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2)  # Discount percentage
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    quantity_in_stock = models.IntegerField()

    def __str__(self):
        return self.product.product_name
    

##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########
##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########
##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########------USER BASED MODELS--------##########
class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True) 
    date_ordered=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    order_id=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=[
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
        ],default="Pending")
    
class OrderItems(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.PositiveBigIntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
    
    

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True) 
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True) 
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"
# customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

class Review (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True) 
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    video_review=models.FileField(upload_to="video_review",blank=True,null=True)
    image_review=models.FileField(upload_to="image_review",blank=True,null=True)

    def __str__(self):
        return str(self.video_review)

