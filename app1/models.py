from django.db import models

from auth_app.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')


class Menu(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')


class Promotion(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='promotions')
    image = models.ImageField(null=True, blank=True, upload_to="images/")


# User models
class Owner(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='employees', null=True)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    spent = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
