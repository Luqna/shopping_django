from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail
from .models import Product, Category, Customer


class AdminProduct(admin.ModelAdmin):
    list_display=['id','name','price','category','description']

class AdminCustomer(admin.ModelAdmin):
    list_display=['id','username','password','address','email','bank']

class AdminCart(admin.ModelAdmin):
    list_display=['id','username','product','image','price','quantity']

class AdminOrder(admin.ModelAdmin):
    list_display=['id','user','product_name','qty','price','status','ordered_date']


admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Cart, AdminCart)
admin.site.register(OrderDetail, AdminOrder)
