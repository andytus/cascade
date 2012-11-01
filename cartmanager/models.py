from django.core.exceptions import ValidationError
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.transaction import TransactionManagementError
from django.db.utils import DatabaseError, IntegrityError
from django.utils.timezone import datetime
from django.contrib.localflavor.us.models import PhoneNumberField
from django import forms
import os

#Note: os.path.dirname(__file__) used to upload files into the app directory
UPLOADEDFILES = FileSystemStorage(location= os.path.join(os.path.dirname(__file__), '/uploads'))

class Route(models.Model):
    ROUTE_TYPE = (("General","General"),("Recycling","Recycling"),
                  ("Refuse","Refuse"), ("Yard-Organics","Yard-Organics"))
    #May turn this into a GeoManaged model for GIS capabilities
    route = models.CharField(max_length=15, null=True)
    route_day = models.CharField(max_length=15, null=True)
    route_type = models.CharField(max_length=20, null=True)


class Address(models.Model):
    #Over ride defaults with instance applications.
    CITY = "DEFAULT"
    ST = "NA"
    house_number = models.CharField(max_length=8)
    street_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=25, default=CITY)
    state = models.CharField(max_length=2, default=ST)
    zipcode = models.IntegerField()
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    route = models.ForeignKey(Route, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s, %s" %(str(self.id), self.house_number, self.street_name)

    class Meta:
        abstract = True


class ServiceCenter(models.Model):
    #service center can also be an A&D service center
    pass

class ServiceCenterAddress(Address):
    pass

class CollectionCustomer(models.Model):
    other_system_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=25, default="UNKNOWN")
    last_name = models.CharField(max_length=50, default="UNKNOWN")
    phone_number = PhoneNumberField(null=True)
    email = models.EmailField(max_length=75, null=True)

    def __unicode__(self):
        return "NAME: " + self.first_name + " " + self.last_name

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

class CollectionAddress(Address):
    billing = models.BooleanField(default=True)
    customer = models.ForeignKey(CollectionCustomer)


class Cart(models.Model):
    """
    CART model stores all cart information.
    These fields are loaded from manufacturing:
    1) Size, 2) Cart Type, 3)RFID, 4) Serial Number, 5)Born data, and Owner.
    Location comes from Services Center, A & D or from customer delivery services.
    """
    CART_TYPE = (('Recycle', 'Recycle'), ('Refuse', 'Refuse'), ('Yard-Organics', 'Yard-Organics'), ('Other','Other') )
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


class CartServiceTicket(models.Model):
    SERVICE_TYPE = (("delivery","delivery"), ("swap","swap"), ("removal","removal"),("repair","repair"), ("audit","audit"))
    CART_TYPE = (('recycle', 'recycle'), ('refuse', 'refuse'), ('yard_organics', 'yard_organics'), ('other','other'), ('yard','yard'), ('organics','organics') )
    STATUS = (('requested','requested'),('open','open'),('completed','completed'))

    location = models.ForeignKey(CollectionAddress)
    cart = models.ForeignKey(Cart, null=True, blank=True)

    service_type = models.CharField(max_length=12, choices=SERVICE_TYPE)
    cart_type = models.CharField(max_length=10, choices=CART_TYPE)

    status = models.CharField(default="requested", choices=STATUS, max_length=12)
    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_accessed = models.DateTimeField(auto_now=True)
    #TODO created and completed by.... hook to user.
    #created_by
    #completed_by

    class Meta:
        ordering = ["-date_created"]

    def __unicode__(self):
        return "Service Type: %s, Status: %s, Location: %s" % (self.service_type, self.status, self.location)

class Users(models.Model):
    pass

class UploadFile(models.Model):

    STATUSES = (
        ("PENDING", "PENDING"),
        ("PROCESSED", "PROCESSED"),
        ("FAILED", "FAILED"),
        )
    FILE_KIND = (
        ("CollectionCustomer","Customer"),
        ("Cart","Carts"),
        ("CartTicket","Tickets"),
    )
    #uploaded_by = models.ForeignKey('auth.User')
    size = models.PositiveIntegerField()
    date_uploaded = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, choices=STATUSES, default='PENDING')
    num_records = models.PositiveIntegerField(default=0)
    num_good = models.PositiveIntegerField(default=0)
    num_error = models.PositiveIntegerField(default=0)
    date_start_processing = models.DateTimeField(null=True)
    date_end_processing = models.DateTimeField(null=True)
    total_process_time = models.IntegerField(null=True)
    file_kind = models.CharField(max_length=10, choices=FILE_KIND)

    class Meta:
        abstract = True

    def save_records(self, line):
        pass

    def process(self):
        self.num_records = 0
        self.num_good = 0
        self.num_error = 0

        file = self.file_path
        #Read just the first header row:
        file.readline()
        self.status = 'PROCESSED'
        self.date_start_processing = datetime.now()
        while 1:
            lines = file.readlines(1000000)
            if not lines:
                break
            for line in lines:
                self.save_records(line)
        self.num_records = self.num_good + self.num_error
        self.date_end_processing = datetime.now()
        self.total_process_time = (self.date_end_processing - self.date_start_processing).seconds
        self.save()
        self.file_path.close()
        return self.num_records, self.num_good, self.num_error



class CartsUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="carts")

    def save_records(self, line):
        try:
            rfid, size, cart_type, born_date = line.split(',')
            cart = Cart(rfid=rfid, size=size, cart_type=cart_type, born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
            cart.full_clean()
            cart.save()
            self.num_good += 1
        except (Exception, ValidationError, ValueError, IntegrityError) as e:
            self.status = "FAILED"
            self.num_error +=1
            error_message = e.message
            if e.message_dict:
                for key, value in e.message_dict.iteritems():
                    error_message += "%s: %s " % (str(key).upper(), ','.join(value))
            error = DataErrors(error_message=error_message, error_type = type(e), failed_data=line)
            error.save()

class TicketsUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="Tickets")

    def save_records(self, line):
        try:




class CustomersUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="customers")

    def save_records(self, line):
       try:

           #Customer setup & save:

           systemid, first_name, last_name, phone, email, house_number, street_name,unit,city,\
           state, zipcode, latitude, longitude, recycle, refuse, yard_organics, route, route_day = line.split(',')

           customer = CollectionCustomer(first_name=first_name, last_name=last_name, email=email,
                      other_system_id = systemid, phone_number = phone)
           customer.full_clean()
           customer.save()

           #######################################################################################################

           #Collection_Address setup & save:
           collection_address = CollectionAddress(customer=customer, house_number=house_number,
           street_name=street_name, unit=unit, city=city, zipcode=zipcode, state=state,
           latitude=latitude, longitude=longitude)
           collection_address.full_clean()
           collection_address.save()

           ########################################################################################################

           #Tickets setup & save for Refuse, Recycling, Yard\Organics:
           #Refactor to dictionary for keys, then for values.
           service = "delivery"

           for x in range(int(refuse)):
               CartServiceTicket(cart_type="refuse", service_type = service, location= collection_address).save()
           for x in range(int(recycle)):
               CartServiceTicket(cart_type="recycling", service_type = service, location= collection_address).save()
           for x in range(int(yard_organics)):
               CartServiceTicket(cart_type="yard-organics", service_type = service, location= collection_address).save()

           self.num_good += 1

       except Exception as e:
           #TODO if it fails all records should be deleted (i.e. collection address, customer, and ticket)
           self.status = "FAILED"
           self.num_error +=1
           error = DataErrors(error_message=e, error_type = type(e), failed_data=line)
           error.save()

class TicketsUploadFileForm(forms.Form):
    ticket_file = forms.FileField()

class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()

class CustomerUploadFileForm(forms.Form):
    customer_file = forms.FileField()

class DataErrors(models.Model):
    #TODO Add datetime stamp and order by it in meta
    error_message = models.CharField(max_length=200)
    error_type = models.CharField(max_length=50)
    failed_data = models.CharField(max_length=500)
    error_date = models.DateTimeField(auto_now_add=True)
    fix_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-error_date"]

    def __unicode__(self):
        return "%s, %s" %(self.error_date, self.error_message)










