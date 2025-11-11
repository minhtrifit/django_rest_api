"""
URL configuration for django_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import product_controller, category_controller, auth_controller, payment_method_controller, order_controller

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Categories
    path('categories', category_controller.get_list),
    path('categories/create', category_controller.create_category),
    path('categories/update/<path:id>', category_controller.update_category),

    # Products
    path('products', product_controller.get_list),
    path('products/detail/<path:id>', product_controller.get_detail),
    path('products/create', product_controller.create_product),
    path('products/update/<path:id>', product_controller.update_product),

    # Auth
    path('auth/register', auth_controller.create_user),
    path('auth/login', auth_controller.login),
    path('auth/profile', auth_controller.get_profile),

    # Payment method
    path('payment_methods', payment_method_controller.get_list),
    path('payment_methods/create', payment_method_controller.create_payment_method),

    # Order
    path('orders', order_controller.get_list),
    path('orders/create', order_controller.create_order),
]