from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.core.files.storage import FileSystemStorage
import datetime
from django import forms
import os

#Note: os.path.dirname(__file__) used to upload files into the app directory
UPLOADEDFILES = FileSystemStorage(location= os.path.dirname(__file__) + '/uploads')

class Address(models.Model):

    class Meta:
        abstract = True


class ServiceCenter(models.Model):
    #service center can also be an A&D service center
    pass

class ServiceCenterAddress(Address):
    pass

class Owner(models.Model):
    customer_number = models.CharField(max_length=25, unique=True)

class OwnerAddress(Address):
    pass

class CollectionCustomer(models.Model):
    pass

class CollectionAddress(Address):
    ADDRESS_TYPE = (('Billing', 'Billing'), ('Location', 'Location') )
    pass

class Cart(models.Model):

    """
    CART model stores all cart information.
    These fields are loaded from manufacturing:
    1) Size, 2) Cart Type, 3)RFID, 4) Serial Number, 5)Born data, and Owner.
    Location comes from Services Center, A & D or from customer delivery services.
    """

    CART_TYPE = (('Recycle', 'Recycle'), ('Refuse', 'Refuse'), ('Yard Waste', 'Yard Waste'), ('Other','Other') )
    CART_SIZE = ((35, 35), (64, 64), (96, 96))
    owner = models.OneToOneField(Owner, on_delete=DO_NOTHING, to_field='customer_number')
    location = models.ForeignKey(CollectionAddress, null=True)
    rfid = models.CharField(max_length=30, unique=True)
    serial_number = models.CharField(max_length=30)
    size = models.IntegerField(choices=CART_SIZE)
    current_status = models.CharField(max_length=30)
    cart_type = models.CharField(max_length=25, choices=CART_TYPE)
    last_updated = models.DateTimeField(auto_now=True)
    born_date = models.DateTimeField()

    def __unicode__(self):
        return "RFID: %s and Type: %s" % (self.rfid, self.cart_type)


class CartServices(models.Model):
    #Will contain the history as query of closed
    pass

class CartTickets(models.Model):
    pass

class Users(models.Model):
    pass

class UploadFile(models.Model):
    STATUSES = (
        ("PENDING", "PENDING"),
        ("PROCESSED", "PROCESSED"),
        ("FAILED", "FAILED"),
        )
    #uploaded_by = models.ForeignKey('auth.User')
    size = models.PositiveIntegerField()
    date_uploaded = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, choices=STATUSES, default='PENDING')
    num_records = models.PositiveIntegerField(default=0)
    date_start_processing = models.DateTimeField(null=True)
    date_end_processing = models.DateTimeField(null=True)

    class Meta:
        abstract = True

class CartsUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="test")

class TicketsUploadFile(UploadFile):
    pass

class CustomersUploadFile(UploadFile):
    pass


class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()








