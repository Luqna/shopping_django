from django.contrib import admin
from django.urls import path
from .views import home, signup, login
from store import views

urlpatterns =[
    path('',views.home, name='homepage'),
    path('signup',views.signup.as_view(),name='signup' ),
    path('login',views.login.as_view(),name='login'),
    path('product-detail/<int:pk>',views.productdetail,name='product-detail'),
    path('logout',views.logout,name='logout'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('plus_cart', views.plus_cart, name='plus_cart'),
    path('minus_cart', views.minus_cart, name='minus_cart'),  # New URL
    path('remove_cart', views.remove_cart, name='remove_cart'),  # New URL
    path('checkout', views.checkout, name='checkout'),  # New URL
    path('order/', views.order, name='order'),  # New URL
]
