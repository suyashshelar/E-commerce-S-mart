from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    details=models.CharField(max_length=1000)
    price=models.IntegerField()
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    pid=models.ForeignKey(Products,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity=models.IntegerField(default=1)

class Address11(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    name=models.CharField(max_length=50)
    mobile_number=models.CharField(max_length=10)
    pincode=models.IntegerField(6)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=30, default=None)
    state=models.CharField(max_length=30)

class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey(User,on_delete = models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products,on_delete = models.CASCADE,db_column='pid')
    quantity=models.IntegerField()