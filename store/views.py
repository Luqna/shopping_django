from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.order import OrderDetail
from .models.cart import Cart
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

################### HOME PAGE
def home(request):
    products = None
    totalitem = 0
    if request.session.has_key('username'):
        username = request.session['username']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(username=username)
        totalitem = len(Cart.objects.filter(username=username))
        for c in customer:
            username = c.username
            categoryID = request.GET.get('category')
            if categoryID:
                products = Product.get_all_product_by_category_id(categoryID)
            else:
                products = Product.get_all_products()
            
            # Format harga
            for product in products:
                product.price = "{:,.0f}".format(int(product.price)).replace(",", ".")
            
            data = {
                'username': username,
                'product': products,
                'category': category,
                'totalitem':totalitem
            }
            print('You are', request.session.get('username'))
            return render(request, 'home.html', data)
    else:
        return redirect('login')


################### SIGN UP
class signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        address = postData.get('address')
        email = postData.get('email')
        bank = postData.get('bank')

        error_message = None
        value = {
            'password': password,
            'username': username,
            'address': address,
            'email': email,
            'bank': bank
        }
        customer = Customer(username=username, password=password, address=address, email=email, bank=bank)

        if not username:
            error_message = 'Name is required'
        elif not password:
            error_message = 'Password is required'
        elif len(password) < 4:
            error_message = 'Password must be more than 4 characters'
        elif customer.isExists():
            error_message = "Username already exists"
        
        if not error_message:
            messages.success(request, 'Register Success')
            customer.register()
            return redirect('signup')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)


################### LOGIN
class login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error_message = None
        value = {
            'username': username,
            'password': password
        }
        customer = Customer.objects.filter(username=username, password=password)
        if customer:
            request.session['username'] = username
            return redirect('homepage')
        else:
            error_message = 'Username or Password is Invalid'
            data = {
                'error': error_message,
                'value': value
            }
        return render(request, 'login.html', data)


################### PRODUCT DETAIL
def productdetail(request, pk):
    totalitem = 0
    product = get_object_or_404(Product, pk=pk)
    item_already_in_cart = False

    # Inisialisasi username dengan None
    username = None

    if request.session.has_key('username'):
        username = request.session['username']
        totalitem = len(Cart.objects.filter(username=username))
        # Memeriksa apakah produk sudah ada di cart
        item_already_in_cart = Cart.objects.filter(Q(product=product) & Q(username=username)).exists()

        customer = Customer.objects.filter(username=username)
        for c in customer:
            username = c.username  # Jika perlu, bisa dihapus jika sudah ada dari session

    # Format harga
    product.price = "{:,.0f}".format(int(product.price)).replace(",", ".")

    data = {
        'product': product,
        'item_already_in_cart': item_already_in_cart,
        'username': username,  # Pastikan username selalu didefinisikan
        'totalitem': totalitem
    }
    return render(request, 'productdetail.html', data)

################### LOGOUT
def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        return redirect('login')
    else:
        return redirect('login')


################### ADD TO CART
def add_to_cart(request):
    username = request.session.get('username')
    product_id = request.POST.get('prod_id')
    product_name = Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)
    for p in product:
        price = p.price
        Cart(username=username, product=product_name,price=price).save()
        return redirect(f'product-detail/{product_id}')


def show_cart(request):
    totalitem = 0
    if request.session.has_key('username'):
        username = request.session['username']
        totalitem = len(Cart.objects.filter(username=username))
        customer = Customer.objects.filter(username=username)
        for c in customer:
            username=c.username
            cart = Cart.objects.filter(username=username)
            data = {
                'username': username,
                'totalitem': totalitem,
                'cart': cart
            }
            if cart:
                return render(request, 'show_cart.html',data)
            else:
                return render(request, 'empty_cart.html',data)
                

def plus_cart(request):
    if request.session.has_key('username'):
        username = request.session['username']
        product_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(username=username))
        cart.quantity+=1
        cart.save()
        data ={
             'quantity':cart.quantity,
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.session.has_key('username'):
        username = request.session['username']
        product_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(username=username))
        cart.quantity-=1
        cart.save()
        data ={
             'quantity':cart.quantity,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.session.has_key('username'):
        username = request.session['username']
        product_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(username=username))
        cart.delete()
        return JsonResponse()


def checkout(request):
    totalitem=0
    if request.session.has_key('username'):
        username = request.session['username']
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        cart_product = Cart.objects.filter(username=username)
        for c in cart_product:
            qty = c.quantity
            price = c.price
            product_name = c.product
            OrderDetail(user=username, product_name=product_name, qty=qty, price=price).save()
            cart_product.delete()
            totalitem = len(Cart.objects.filter(username=username))
            customer = Customer.objects.filter(username=username)
            for c in customer:
                username=c.username
            data={
                'name':name,
                'totalitem':totalitem
            }
            return render(request, 'empty_cart.html',data)
    else:
        return redirect('login')
        
        
    
