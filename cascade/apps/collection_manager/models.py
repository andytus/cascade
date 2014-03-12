from django.db import models

# Create your models here.


class Collection(models.Model):
    rfid = models.CharField(max_length=30)
    pickup_date = models.DateTimeField()
    loaded_date = models.DateTimeField(auto_now=True)


class Vehicles(models.Model):
    name = models.CharField(max_length=25)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

