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
import requests
import datetime
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

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
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    context = {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro}
    return render(request, "about.html", context)

def shop(request):
    product = Product.objects.all()
    num_objects = product.count()
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    context = {"product":product, "num_objects":num_objects, "no_of_cartpro":no_of_cartpro, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,}
    return render(request, "shop.html", context)

def sort_product(request):
    product = Product.objects.all()
    num_objects = product.count()
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    context = {"product":product, "num_objects":num_objects, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,}
    if request.method == "POST":
        sort = request.POST.get("sort")
        if sort == "none":
            return render(request, "shop.html", context)
        elif sort == "acending":
            product_ace = Product.objects.all().order_by("price")
            return render(request, "shop.html", {"product":product_ace})
        elif sort == "dicending":
            product_dec = Product.objects.all().order_by("price").reverse()
            return render(request, "shop.html", {"product":product_dec, "no_of_cartpro":no_of_cartpro})
        else:
            return render(request, "shop.html", context)
    return render(request, "shop.html", context)


def shop_detail(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    return render(request, "shop_detail.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})

def cart(request, id):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    product = Product.objects.get(id=id)
    products = Cart.objects.filter(usr=request.user.id)
    addtocart = Cart(product=product, usr=request.user)
    addtocart.save()
    total_price = 0
    for i in products:
        total_price = total_price + i.product.price
    context = {"products":products, "total_price":total_price, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,}
    return render(request, "cart.html", context)


def my_cart(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    products = Cart.objects.filter(usr=request.user.id)
    total_price = 0
    for i in products:
        total_price = total_price + i.product.price
    context = {"products":products, "total_price":total_price, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,}
    return render(request, "cart.html", context)

def cartdelete(request, id):
    product = Cart.objects.filter(product=id).first()
    product.delete()
    return redirect('my_cart')

def checkout(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    return render(request, "checkout.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro})

def my_account(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        account = Account(name=name, last_name=last_name, email=email, phone_number=phone_number, usr=request.user)
        account.save()
        messages.info(request, "Account Created Successfully...")
    if Account.objects.filter(usr=request.user).exists():
        the_account = Account.objects.filter(usr=request.user).first()
        return render(request, "my_account.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,"the_account":the_account})
    else:
        return render(request, "my_account.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})

def wishlist(request):
    cartproduct = Cart.objects.filter(usr=request.user)
    no_of_cartpro = cartproduct.count()
    return render(request, "wishlist.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})

def gallery(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    return render(request, "gallery.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})

def contact_us(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    return render(request, "contact_us.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})

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

def weather(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    api_key = 'de3a7d0c8eac74b9712c0beae0f744ec'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
            "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,
        }

        return render(request, 'weather.html', context)
    else:
        return render(request, 'weather.html', {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro,})
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=de3a7d0c8eac74b9712c0beae0f744ec".format(lat,lon)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    # print(forecast_response)

    daily_forecasts = []
    for daily_data in forecast_response['list'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['main']['temp_min'] - 273.15, 2),
            'max_temp': round(daily_data['main']['temp_max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })
    # print(daily_forecasts)
    return weather_data, daily_forecasts

def neutrition_deficiency(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    if request.method == "POST":
        image = request.FILES["image"]
        # Define a function to extract features from an image
        def extract_features(image_path):
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            return hist.flatten()

        # Load and preprocess your dataset of labeled plant images
        def load_dataset(dataset_dir):
            labels = []
            data = []

            for label in os.listdir(dataset_dir):
                label_dir = os.path.join(dataset_dir, label)
                for image_file in os.listdir(label_dir):
                    image_path = os.path.join(label_dir, image_file)
                    features = extract_features(image_path)
                    data.append(features)
                    labels.append(label)

            le = LabelEncoder()
            labels = le.fit_transform(labels)
            return np.array(data), np.array(labels), le

        # Load your dataset
        dataset_dir = "C:/Users/ThinkPad/Desktop/Zion_projects/SEPTEMBER/Farmer's Ecommerce/farmerpro/rice_plant_lacks_nutrients"
        data, labels, le = load_dataset(dataset_dir)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

        # Train a machine learning classifier (Random Forest, in this case)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = clf.predict(X_test)

        # Evaluate the classifier
        print(classification_report(y_test, y_pred))

        # Define a function to predict nutrition deficiencies in a new image
        def predict_deficiency(image_path, clf, le):
            features = extract_features(image_path)
            label = clf.predict([features])[0]
            label = le.inverse_transform([label])[0]
            return label

        # Create a unique filename for the uploaded image
        uploaded_image_path = os.path.join(settings.MEDIA_ROOT, "uploaded_images", image.name)
        uploaded_image_path = uploaded_image_path.replace("\\", "/")

        # Save the uploaded image to the specified path
        with open(uploaded_image_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        predicted_deficiency = predict_deficiency(uploaded_image_path, clf, le)
        print(f"Predicted deficiency: {predicted_deficiency}")
        return render(request, "output.html", {"classification_report":classification_report(y_test, y_pred), "predicted_deficiency":predicted_deficiency, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro})
    return render(request, "input.html", {"predicted_deficiency":predicted_deficiency, "cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro})

def add_product(request):
    cartproduct = Cart.objects.filter(usr=request.user.id)
    no_of_cartpro = cartproduct.count()
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES['image']
        description = request.POST.get("description")
        price = request.POST.get("price")
        product = Product(name=name, image=image, discription=description, price=price, usr=request.user)
        product.save()
        messages.info(request, "{} added successfuly...".format(name))
        return redirect("index")
    return render(request, "addproduct.html", {"cartproduct":cartproduct, "no_of_cartpro":no_of_cartpro })