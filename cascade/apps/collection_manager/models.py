from django.db import models

# Create your models here.


class Collection(models.Model):
    rfid = models.CharField(max_length=30)
    pickup_date = models.DateTimeField()
    loaded_date = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)


class Vehicle(models.Model):
    name = models.CharField(max_length=25)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

class VehicleCollectionHistoryFile(models.Model):
    pass

