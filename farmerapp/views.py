from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.

@csrf_exempt
def index(request):
    products = Product.objects.all()
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    context = {"products":products, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro}
    return render(request, "index.html", context)

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password incorrect')
            return render(request, "login.html")
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Taken")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Both passwords are not matching")
            return render(request, "register.html")
    return render(request, "register.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def about(request):
    return render(request, "about.html")

def shop(request):
    product = Product.objects.all()
    num_objects = product.count()
    context = {"product":product, "num_objects":num_objects}
    return render(request, "shop.html", context)

def sort_product(request):
    product = Product.objects.all()
    num_objects = product.count()
    context = {"product":product, "num_objects":num_objects}
    if request.method == "POST":
        sort = request.POST.get("sort")
        if sort == "none":
            return render(request, "shop.html", context)
        elif sort == "acending":
            product_ace = Product.objects.all().order_by("price")
            return render(request, "shop.html", {"product":product_ace})
        elif sort == "dicending":
            product_dec = Product.objects.all().order_by("price").reverse()
            return render(request, "shop.html", {"product":product_dec})
        else:
            return render(request, "shop.html", context)
    return render(request, "shop.html", context)


def shop_detail(request):
    return render(request, "shop_detail.html")

def cart(request, id):
    product = Product.objects.get(id=id)
    products = Cart.objects.filter(usr=request.user.id)
    addtocart = Cart(product=product, usr=request.user)
    addtocart.save()
    total_price = 0
    for i in products:
        total_price = total_price + i.product.price
    context = {"products":products, "total_price":total_price}
    return render(request, "cart.html", context)


def my_cart(request):
    products = Cart.objects.filter(usr=request.user.id)
    total_price = 0
    for i in products:
        total_price = total_price + i.product.price
    context = {"products":products, "total_price":total_price}
    return render(request, "cart.html", context)

def cartdelete(request, id):
    product = Cart.objects.filter(product=id).first()
    product.delete()
    return redirect('my_cart')

def checkout(request):
    return render(request, "checkout.html")

def my_account(request):
    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        account = Account(name=name, last_name=last_name, email=email, phone_number=phone_number, usr=request.user)
        account.save()
        messages.info(request, "Account Created Successfully...")
    return render(request, "my_account.html")

def wishlist(request):
    return render(request, "wishlist.html")

def gallery(request):
    return render(request, "gallery.html")

def contact_us(request):
    return render(request, "contact_us.html")

def payment(request,id):
    item = Product.objects.get(id=id)
    currency = 'INR'
    amt = item.price
    product = Cart.objects.filter(product=id, usr=request.user.id).first()
    product.payment_status = True
    product.save()
    amount = amt * 100
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                        currency=currency,
                        payment_capture='0'))
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'http://127.0.0.1:8000/index'
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1"
    return render(request, "payment.html",context)
