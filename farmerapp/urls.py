from django.urls import path
from farmerapp import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('index',views.index, name="index"),
    path('logout', views.logout, name="logout"),
    path('sort_product', views.sort_product, name="sort_product"),
    path('my_cart', views.my_cart, name="my_cart"),
    path('payment/<int:id>', views.payment, name="payment"),
    path('about', views.about, name="about"),
    path('shop', views.shop, name="shop"),
    path('shop_detail', views.shop_detail, name="shop_detail"),
    path('cart/<int:id>', views.cart, name="cart"),
    path('cartdelete/<int:id>', views.cartdelete, name="cartdelete"),
    path('cartdelete/<int:id>', views.cartdelete, name="cartdelete"),
    path('checkout', views.checkout, name="checkout"),
    path('my_account', views.my_account, name="my_account"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('gallery', views.gallery, name="gallery"),
    path('contact_us', views.contact_us, name="contact_us"),
]