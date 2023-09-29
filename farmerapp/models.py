from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Product_image")
    discription = models.CharField(max_length=250)
    price = models.IntegerField()
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    payment_status = models.BooleanField(default=False, null=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
class Account(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13)
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name