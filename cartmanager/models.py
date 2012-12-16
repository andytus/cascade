from django.core.exceptions import ValidationError
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db.transaction import TransactionManagementError
from django.db.utils import DatabaseError, IntegrityError
from django.utils.timezone import datetime
from django.contrib.localflavor.us.models import PhoneNumberField
from django import forms
import os

#Note: os.path.dirname(__file__) used to upload files into the app directory
UPLOADEDFILES = FileSystemStorage(location= os.path.join(os.path.dirname(__file__), 'uploads'))


class Route(models.Model):
    ROUTE_TYPE = (("General","General"),("Recycling","Recycling"),
                  ("Refuse","Refuse"), ("Yard-Organics","Yard-Organics"))
    #May turn this into a GeoManaged model for GIS capabilities
    route = models.CharField(max_length=15, null=True)
    route_day = models.CharField(max_length=15, null=True)
    route_type = models.CharField(max_length=20, null=True)
    #TODO def get_absolute_url

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

    def get_coordinates(self):
        coordinates = {"type":"Feature", "geometry": {"type": "Point", "coordinates": [float(self.latitude or 0), float(self.longitude or 0)]}}
        return coordinates

    def get_absolute_url(self):
        return reverse('location_api_profile', args=[str(self.id)])

    def get_info(self):
        info = {"properties":{"url": self.get_absolute_url(),"id":self.id, "house_number":self.house_number, "unit":self.unit, "street_name":self.street_name,
                "city":self.city, "state":self.state, "zipcode":self.zipcode},"type":"Feature", "geometry":
                {"type": "Point", "coordinates": [float(self.latitude or 0), float(self.longitude or 0)]} }

        return info

    def __unicode__(self):
        return "%s %s" %(self.house_number, self.street_name)

    #TODO def get_absolute_url

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

    def get_absolute_url(self):
        return reverse('customer_api_profile', args=[str(self.id)])

    def get_info(self):
        info = {"id":self.id, "name":self.full_name, "url": self.get_absolute_url()}
        return info

class CollectionAddress(Address):
    ADDRESS_TYPE = (('Inventory', 'Inventory'), ('Billing', 'Billing'))
    type = models.CharField(max_length=9, choices=ADDRESS_TYPE, default='Billing')
    customer = models.ForeignKey(CollectionCustomer, null=True, blank=True)

class Cart(models.Model):
    """
    CART model stores all cart information.
    These fields are loaded from manufacturing:
    1) Size, 2) Cart Type, 3)RFID, 4) Serial Number, and 5)Born data
    Location comes from Services Center, A & D or from customer delivery services.
    """
    CART_TYPE = (('Recycle', 'Recycle'), ('Refuse', 'Refuse'), ('Yard-Organics', 'Yard-Organics'), ('Other','Other') )
    CART_SIZE = ((35, 35), (64, 64), (96, 96))
    location = models.ForeignKey(CollectionAddress, null=True, blank=True, related_name='location')
    last_latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    rfid = models.CharField(max_length=30, unique=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    size = models.IntegerField(choices=CART_SIZE)
    current_status = models.CharField(max_length=30, null=True, blank=True)
    cart_type = models.CharField(max_length=25, choices=CART_TYPE)
    last_updated = models.DateTimeField(auto_now=datetime.now)
    born_date = models.DateTimeField()

    def __unicode__(self):
        return "RFID: %s, Type: %s, PK: %s" % (self.rfid, self.cart_type, self.id)


    def get_absolute_url(self):
        return reverse('cart_api_profile', args=[str(self.id)])

    def get_info(self):
        info =  {"serial":self.serial_number, "id":self.id, "url": self.get_absolute_url(), "cart_type":self.cart_type,
                 "size": self.size, "born_data": self.born_date, "current_status": self.current_status }
        return info

class CartServiceTicket(models.Model):
    SERVICE_TYPE = (("delivery","delivery"), ("swap","swap"), ("removal","removal"),("repair","repair"),
                   ("audit","audit"))
    CART_TYPE = (('recycle', 'recycle'), ('refuse', 'refuse'), ('yard_organics', 'yard_organics'), ('other','other'),
                 ('yard','yard'), ('organics','organics') )
    STATUS = (('requested','requested'),('open','open'),('completed','completed'), ('unsuccessful', 'unsuccessful'))
    AUDIT_STATUS = (('No Change','No Change'), ('Changed','Changed'))

    location = models.ForeignKey(CollectionAddress)
    cart = models.ForeignKey(Cart, null=True, blank=True)

    service_type = models.CharField(max_length=12, choices=SERVICE_TYPE)
    cart_type = models.CharField(max_length=10, choices=CART_TYPE)

    status = models.CharField(default="requested", choices=STATUS, max_length=12)
    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_accessed = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    device_name = models.CharField(max_length=50, null=True, blank=True)
    swap_to_rfid = models.CharField(max_length=24, null=True, blank=True)
    success_attempts = models.IntegerField()
    audit_status = models.CharField(max_length=15, null=True, blank=True, choices=AUDIT_STATUS)
    broken_component = models.CharField(max_length=60, null=True, blank=True)
    broken_comments = models.CharField(max_length=60, null=True, blank=True)
    #TODO created and completed by.... hook to user.
    #TODO going to need reason code for incomplete
    #created_by
    #completed_bys
    #TODO def get_absolute_url

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
    message = models.CharField(max_length=200, null=True, blank=True)

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
            rfid, serial, size, cart_type, born_date = line.split(',')
            cart = Cart(rfid=rfid, serial_number=serial, size=size, cart_type=cart_type, current_status='born', born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
            cart.location = CollectionAddress.objects.get(pk=1)
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

            #TODO def get_absolute_url

class TicketsCompleteUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="Tickets")
    swap_count = models.IntegerField(default=0)
    delivery_count = models.IntegerField(default=0)
    removal_count = models.IntegerField(default=0)
    audit_count = models.IntegerField(default=0)
    unsucessful = models.IntegerField(default=0)
    repair_count = models.IntegerField(default=0)

    def save_records(self, line):
        try:
            #Get imported files data
            system_id, street, house_number, unit_number, container_size, container_type, rfid, status, service_type, \
            complete_datetime, device_name, lat, lon, broken_component, broken_comments = line.split(',')

            ticket = CartServiceTicket.objects.get(id=system_id)
            time_format = '%m/%d/%Y %H:%M' #matches time as 11/1/2012 15:20

            #check for status complete, because you don't want to over write already completed tickets.
            if ticket.status != 'completed':

                if lat and lon:
                    ticket.latitude = lat
                    ticket.longitude = lon

                #status from the upload file
                if status == "COMPLETED":
                    cart = Cart.objects.get(rfid__exact=rfid)
                    if lat and lon:
                        cart.last_latitude = lat
                        cart.last_longitude = lon
                    if "delivery" in ticket.service_type:
                        self.delivery_count += 1
                        ticket.cart = cart
                        cart.current_status = "delivered"

                    elif "swap" in ticket.service_type or  "removal" in ticket.service_type:
                        #check to see if the swapped cart is still at the ticket location before removing

                        if ticket.cart.location == ticket.location:
                            ticket.cart.location = None
                            ticket.cart.current_status = "inventory"
                            ticket.cart.save()

                        if "swap" in ticket.service_type:
                            #add the rfid of the swapped to rfid
                            self.swap_count += 1
                            ticket.swap_to_rfid = cart.rfid
                            cart.current_status = "delivered"
                            cart.location = ticket.location
                        else:
                            self.removal_count += 1

                    elif  "audit" in ticket.service_type:
                        self.audit_count +=1
                        #check to see if the cart was changed
                        if ticket.cart == cart:
                            ticket.audit_status = "No Change"
                        else:
                            cart.location = ticket.location
                            cart.current_status = "delivered"
                            ticket.swap_to_rfid = cart.rfid
                            ticket.audit_status = "Changed"

                    elif "repair" in ticket.service_type:
                        self.repair_count +=1
                        ticket.broken_component = broken_component
                        ticket.broken_commens = broken_comments


                    ticket.date_completed= datetime.strptime(complete_datetime.strip(), time_format)
                    ticket.device_name = device_name
                    ticket.status = "completed"
                    ticket.success_attempts += 1
                    cart.save()

                elif status == "UNSUCCESSFUL":
                    ticket.status = "unsuccessful"
                    ticket.success_attempts +=1
                else:
                    pass

                ticket.save()
            self.num_good += 1


        except (Exception, ValidationError, ValueError, IntegrityError) as e:

            self.status = "FAILED"
            self.num_error +=1
            error_message = e.message
            print error_message
            if hasattr(e, 'message_dict'):
                for key, value in e.message_dict.iteritems():
                    error_message += "%s: %s " % (str(key).upper(), ','.join(value))
            error = DataErrors(error_message=error_message, error_type = type(e), failed_data=line)
            error.save()

            #TODO def get_absolute_url

class CustomersUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="customers")

    #TODO def get_absolute_url

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

class TicketsCompletedUploadFileForm(forms.Form):
    ticket_file = forms.FileField()

class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()

class CustomerUploadFileForm(forms.Form):
    customer_file = forms.FileField()

class DataErrors(models.Model):
    #TODO def get_absolute_url
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










