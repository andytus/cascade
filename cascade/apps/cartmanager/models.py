from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db.utils import DatabaseError, IntegrityError
from django.utils.timezone import datetime
from django.contrib.localflavor.us.models import PhoneNumberField
from django import forms

import os

#Note: os.path.dirname(__file__) used to upload files into the app directory
SITE = Site.objects.get_current()
UPLOADEDFILES = FileSystemStorage(location= os.path.join(os.path.dirname(__file__), 'uploads_' + SITE.domain))

def save_error(e, line):
    error_message = e.message
    print error_message
    if hasattr(e, 'message_dict'):
        for key, value in e.message_dict.iteritems():
            error_message += "%s: %s " % (str(key).upper(), ','.join(value))
    Site.objects.clear_cache()
    error = DataErrors(error_message=error_message, error_type = type(e), failed_data=line, site=Site.objects.get_current())
    error.save()


class CartStatus(models.Model):
    LEVEL = (("label-warning", "Warning"), ("label-info", "Info"), ("label-important", "Alert"), ("label-success","Success" ),
             ("label-inverse", "Default"), ('label', 'Inverse'))
    level = models.CharField(max_length=25, choices=LEVEL)
    label = models.CharField(max_length=35)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "%s, %s" % (self.level, self.label)

class CartType(models.Model):
     name = models.CharField(max_length=20)
     size = models.IntegerField()
     #model managers:
     site = models.ForeignKey(Site)
     objects = models.Manager()
     on_site = CurrentSiteManager()

     def get_info(self):
         return {'name':self.name, 'size': self.size}

     def __unicode__(self):
         return "%s" % (self.name)


class CartServiceStatus(models.Model):
    LEVEL = (("label-warning", "Warning"), ("label-info", "Info"), ("label-important", "Alert"), ("label-success","Success" ),
             ("label-inverse", "Default"), ('label', 'Inverse'))
    level = models.CharField(max_length=35, choices=LEVEL)
    service_status = models.CharField(max_length=30)


    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "%s, %s" % (self.service_status, self.level)


class CartServiceType(models.Model):
    SERVICE_CODE = (('REM-DEL', 'REM-DEL'), ('DEL','DEL'), ('REM', 'REM'), ('REPAIR', 'REPAIR'), ('AUDIT', 'AUDIT'))
    service = models.CharField(max_length=25)
    code = models.CharField(max_length=15, choices=SERVICE_CODE)
    description = models.TextField(max_length=300, null=True)
    complete_cart_status_change = models.ForeignKey(CartStatus)

    #model Managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'service': self.service, 'code': self.code, 'description': self.description}

    def __unicode__(self):
         return "%s" % (self.service)


class Route(models.Model):
    ROUTE_TYPE = (("General","General"),("Recycling","Recycling"),
                  ("Refuse","Refuse"), ("Yard-Organics","Yard-Organics"))
    #May turn this into a GeoManaged model for GIS capabilities
    route = models.CharField(max_length=15, null=True)
    route_day = models.CharField(max_length=15, null=True)
    route_type = models.CharField(max_length=20, null=True)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()


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

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()


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
    other_system_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=25, default="UNKNOWN")
    last_name = models.CharField(max_length=50, default="UNKNOWN")
    phone_number = PhoneNumberField(max_length=15, null=True)
    email = models.EmailField(max_length=75, null=True)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()




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
    CART_SIZE = ((35, 35), (64, 64), (96, 96))
    location = models.ForeignKey(CollectionAddress, null=True, blank=True, related_name='location')
    last_latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    rfid = models.CharField(max_length=30, unique=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    size = models.IntegerField(choices=CART_SIZE)
    current_status = models.ForeignKey(CartStatus, null=True, blank=True)
    cart_type = models.ForeignKey(CartType, null=True, blank=True, default=1)
    last_updated = models.DateTimeField(auto_now=datetime.now)
    born_date = models.DateTimeField()

    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()


    def __unicode__(self):
        return "rfid: %s, Type: %s, PK: %s" % (self.rfid, self.cart_type, self.id)


    def get_absolute_url(self):
        return reverse('cart_api_profile', args=[str(self.id)])

    def get_info(self):
        info =  {'rfid': self.rfid, "serial":self.serial_number, "id":self.id, "url": self.get_absolute_url(), "cart_type":self.cart_type.name,
                 "size": self.size, "born_date": self.born_date, "current_status": self.current_status.label, "current_status_level": self.current_status.level }
        return info

class CartServiceTicket(models.Model):

    AUDIT_STATUS = (('No Change','No Change'), ('Changed','Changed'))


    delivered_cart = models.ForeignKey(Cart, null=True, blank=True, related_name='delivered_cart')
    removed_cart = models.ForeignKey(Cart, null=True, blank=True, related_name='removed_cart')
    audit_cart = models.ForeignKey(Cart, null=True, blank=True, related_name='audit_cart')

    location = models.ForeignKey(CollectionAddress, related_name="address")
    service_type = models.ForeignKey(CartServiceType, null=True, blank=True, related_name="service_type")
    cart_type = models.ForeignKey(CartType, null=True, blank=True, related_name="cart_type")
    status = models.ForeignKey(CartServiceStatus, null=True, blank=True, related_name="status")


    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_accessed = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    device_name = models.CharField(max_length=50, null=True, blank=True)
    success_attempts = models.IntegerField(default=0)
    audit_status = models.CharField(max_length=15, null=True, blank=True, choices=AUDIT_STATUS)
    broken_component = models.CharField(max_length=60, null=True, blank=True)
    broken_comments = models.CharField(max_length=60, null=True, blank=True)

    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()



    #TODO created and completed by.... hook to user.
    #TODO going to need reason code for incomplete
    #created_by
    #completed_bys
    #TODO def get_absolute_url

    class Meta:
        ordering = ["-date_created"]

    def __unicode__(self):
        return "Service Type: %s, Status: %s, Location: %s" % (self.service_type, self.status, self.location)

class UserAccountProfile(models.Model):
    user = models.OneToOneField(User)
    sites = models.ManyToManyField(Site)
    company = models.CharField(max_length=50, null=True)
    objects = models.Manager()
    on_site = CurrentSiteManager()



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

    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    def save_records(self, line, site):
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
                self.save_records(line, self.site)
        self.num_records = self.num_good + self.num_error
        self.date_end_processing = datetime.now()
        self.total_process_time = (self.date_end_processing - self.date_start_processing).seconds
        self.save()
        self.file_path.close()
        return self.num_records, self.num_good, self.num_error

class CartsUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="carts")

    def save_records(self, line, site):
        try:
            #default status is produced
            status = CartStatus.objects.get(pk=2)
            rfid, serial, size, cart_type, born_date = line.split(',')
            #get cart type by name
            cart_type = CartType.objects.filter(name=cart_type)
            cart = Cart(site=site, rfid=rfid, serial_number=serial, size=size, cart_type=cart_type, current_status=status, born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
            cart.location = CollectionAddress.objects.get(pk=1)
            cart.full_clean()
            cart.save()
            self.num_good += 1
        except (Exception, ValidationError, ValueError, IntegrityError) as e:
            self.status = "FAILED"
            self.num_error +=1
            save_error(e, line)
            #TODO def get_absolute_url

class TicketsCompleteUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="Tickets")
    delivery_count = models.IntegerField(default=0)
    removal_count = models.IntegerField(default=0)
    audit_count = models.IntegerField(default=0)
    adhoc_count = models.IntegerField(default=0)
    unsucessful = models.IntegerField(default=0)
    repair_count = models.IntegerField(default=0)

    def save_records(self, line, site):
        try:
            #Get imported files data
            system_id, street, house_number, unit_number, container_size, container_type, rfid, upload_ticket_status, service_type, \
            complete_datetime, device_name, lat, lon, broken_component, broken_comments = line.split(',')

            ticket = CartServiceTicket.on_site.get(site=site, id=system_id)
            #Cart Service status object
            time_format = '%m/%d/%Y %H:%M' #matches time as 11/1/2012 15:20

            #check for status complete, because you don't want to over write already completed tickets.
            if ticket.status.service_status != 'completed':

                if lat and lon:
                    ticket.latitude = lat
                    ticket.longitude = lon

                #status from the upload file
                if upload_ticket_status == "COMPLETED":
                    cart = Cart.objects.get(rfid__exact=rfid)
                    cart.current_status = ticket.cartservicetype.complete_cart_status_change

                    if lat and lon:
                        cart.last_latitude = lat
                        cart.last_longitude = lon

                    #For Deliveries
                    if  ticket.service_type.code == 'DEL':
                        ticket.delivered_cart = cart
                        cart.location = ticket.location
                        self.delivery_count += 1

                    #For Removals and Swaps (REM-DEL)
                    elif ticket.service_type.code == 'REM-DEL' or  ticket.service_type.code == 'REM':
                        #check to see if the swapped(REM-DEL) cart is still at the ticket location before removing
                        #Because it could have been delivered to another address
                        if ticket.removed_cart.location == ticket.location:
                            #if the removed cart associated with the ticket is still located in the database at the location
                            #associated with the ticket, then simply place it in inventory and change its status!
                            ticket.removed_cart.location = CollectionAddress.on_site.get(type='Inventory')
                            ticket.removed_cart.current_status = CartStatus.on_site.get(label="Inventory")
                            ticket.removed_cart.save()
                            self.removal_count += 1

                            if ticket.service_type.code == 'REM-DEL':
                                ticket.delivered_cart = cart
                                cart.location = ticket.location
                                self.delivery_count +=1

                    #For AUDITS
                    elif  ticket.service_type.code == 'AUDIT':
                        self.audit_count +=1
                        #check to see if the cart was changed
                        if ticket.audit_cart == cart:
                            ticket.audit_status = "No Change"
                        else:
                            cart.location = ticket.location
                            ticket.audit_status = "Changed"

                    elif ticket.service_type.code == 'REPAIR':
                        self.repair_count +=1
                        ticket.broken_component = broken_component
                        ticket.broken_comments = broken_comments


                    ticket.date_completed= datetime.strptime(complete_datetime.strip(), time_format)
                    ticket.device_name = device_name
                    ticket.status = CartServiceStatus.on_site.get(service_status='completed')
                    ticket.success_attempts += 1
                    cart.save()

                elif upload_ticket_status == "UNSUCCESSFUL":
                    ticket.status = "unsuccessful"
                    ticket.success_attempts +=1

                elif upload_ticket_status == "ADD":
                    pass

                ticket.save()
            self.num_good += 1


        except (Exception, ValidationError, ValueError, IntegrityError) as e:

            self.status = "FAILED"
            self.num_error +=1
            error_message = e.message
            if hasattr(e, 'message_dict'):
                for key, value in e.message_dict.iteritems():
                    error_message += "%s: %s " % (str(key).upper(), ','.join(value))
            error = DataErrors(error_message=error_message, error_type = type(e), failed_data=line)
            error.save()

            #TODO def get_absolute_url

class CustomersUploadFile(UploadFile):
    file_path = models.FileField(storage=UPLOADEDFILES, upload_to="customers")

    #TODO def get_absolute_url

    def save_records(self, line, site):
       try:
           #Customer setup & save:
           systemid, first_name, last_name, phone, email, house_number, street_name,unit,city,\
           state, zipcode, latitude, longitude, recycle, recycle_size, refuse, refuse_size, yard_organics, \
           yard_organics_size, other, route, route_day = line.split(',')

           customer = CollectionCustomer(site=site,first_name=first_name, last_name=last_name, email=email,
                      other_system_id = systemid, phone_number = phone)

           #.full_clean checks for the correct data
           customer.full_clean()
           customer.save()

           #######################################################################################################

           #Collection_Address setup & save:
           collection_address = CollectionAddress(site=site, customer=customer, house_number=house_number,
                                                  street_name=street_name, unit=unit, city=city, zipcode=zipcode,
                                                  state=state,latitude=latitude, longitude=longitude)
           collection_address.full_clean()
           collection_address.save()

           ########################################################################################################

           #Tickets setup & save for Refuse, Recycling, Other, Yard\Organics:
           #Refactor to dictionary for keys, then for values.
           delivery = CartServiceType.on_site.get(site=site, code="DEL")
           open = CartServiceStatus.on_site.get(site=site, service_status="open")

           for x in range(int(refuse)):
               CartServiceTicket(cart_type=CartType.on_site.get(site=site, name="Refuse"), service_type = delivery, location= collection_address, status=open ).save()
           for x in range(int(recycle)):
               CartServiceTicket(CartType.on_site.get(site=site, name="Recycle"), service_type = delivery, location= collection_address, status=open).save()
           for x in range(int(yard_organics)):
               CartServiceTicket(CartType.on_site.get(site=site, name="Yard-Organics"), service_type = delivery, location= collection_address, status=open).save()
           for x in range(int(other)):
               CartServiceTicket(CartType.on_site.get(site=site, name="Other"), service_type = delivery, location= collection_address, status=open).save()

           self.num_good += 1

       except Exception as e:
           #TODO if it fails all records should be deleted (i.e. collection address, customer, and ticket)
           self.status = "FAILED"
           self.num_error +=1
           error = DataErrors(site=site, error_message=e, error_type = type(e), failed_data=line)
           print error
           error.save()

class DataErrors(models.Model):
    #TODO def get_absolute_url
    error_message = models.CharField(max_length=200)
    error_type = models.CharField(max_length=100)
    failed_data = models.CharField(max_length=500)
    error_date = models.DateTimeField(auto_now_add=True)
    fix_date = models.DateTimeField(null=True)

    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        ordering = ["-error_date"]

    def __unicode__(self):
        return "%s, %s" %(self.error_date, self.error_message)


class TicketsCompletedUploadFileForm(forms.Form):
    ticket_file = forms.FileField()

class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()

class CustomerUploadFileForm(forms.Form):
    customer_file = forms.FileField()











