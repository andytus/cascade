from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import datetime
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
    location = models.ForeignKey(CollectionAddress, null=True, blank=True)
    rfid = models.CharField(max_length=30, unique=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    size = models.IntegerField(choices=CART_SIZE)
    current_status = models.CharField(max_length=30, null=True, blank=True)
    cart_type = models.CharField(max_length=25, choices=CART_TYPE)
    last_updated = models.DateTimeField(default=datetime.now)
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
    total_process_time = models.IntegerField(null=True)

    class Meta:
        abstract = True


class CartsUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="carts")
    def process(self):
        """
        CartsUploadFile.process
        attempts to iterate the uploaded file for cart records
        and saves each cart record to a Cart object hence to the
        database. Attempted to speed this up by reading a certain chuck
        of bytes into memory, processing, and then starting over with a new chunk
        See: https://docs.djangoproject.com/en/dev/ref/models/instances/?from=olddocs#django.db.models.Model.full_clean
        http://effbot.org/zone/readline-performance.htm
        """
        cart_file = self.file_path
        cart_file.readline()
        count_records = 0
        count_error = 0
        self.status = 'PROCESSED'
        self.date_start_processing = datetime.now()
        while 1:
            lines = cart_file.readlines(100000)
            if not lines:
                break
            for line in lines:
                try:
                    rfid, size, cart_type, born_date = line.split(',')
                    cart = Cart(rfid=rfid, size=size, cart_type=cart_type, born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
                    cart.full_clean()
                    cart.save()
                    count_records += 1
                except Exception as e:
                    self.status = 'FAILED'
                    count_records += 1
                    error = DataErrors(error_message=e.message, error_type = type(e), failed_data=line)
                    error.save()
                    print "%s, (%s)" % (e.message, type(e))
        self.num_records = count_records + count_error
        self.date_end_processing = datetime.now()
        self.total_process_time = (self.date_end_processing - self.date_start_processing).seconds
        self.save()
        self.file_path.close()
        #TODO Return a message with counts, and general errors (i.e. already processed)
        return self.num_records, count_records, count_error


            #TODO save error log to table

class TicketsUploadFile(UploadFile):
    pass

class CustomersUploadFile(UploadFile):
    pass


class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()

class DataErrors(models.Model):
    error_message = models.CharField(max_length=200)
    error_type = models.CharField(max_length=50)
    failed_data = models.CharField(max_length=500)





