from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.urlresolvers import reverse
from django.utils.timezone import datetime
from django.contrib.localflavor.us.models import PhoneNumberField
from django import forms

import os


def get_upload_path(instance, filename):
    """
     gets correct path for an uploaded file

    """
    #Note: os.path.dirname(__file__) used to upload files into the app directory
    return os.path.join('uploads', instance.site.domain, instance.file_kind, filename)


class UploadFile(models.Model):
    """
    meta class for all upload models

    Public methods
    ---------------
    process: defines a consistent way of processing all uploaded files.
    save_records: must be implemented in subclasses

    """

    STATUSES = (
        ("PENDING", "PENDING"),
        ("UPLOADED", "UPLOADED"),
        ("FAILURES", "FAILURES"),
    )

    FILE_KIND = (
        ("CollectionCustomer", "Customers"),
        ("Cart", "Carts"),
        ("CartTicket", "Tickets"),
        ("Route", "Route"),
    )

    file_path = models.FileField(upload_to=get_upload_path, max_length=300)
    uploaded_by = models.ForeignKey(User)
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
    records_processed = models.BooleanField(default=False)

    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class RouteUploadFile(UploadFile):
    pass


class CartsUploadFile(UploadFile):
    pass


class CustomersUploadFile(UploadFile):
    pass


class TicketsCompleteUploadFile(UploadFile):
    success_count = models.IntegerField(default=0)
    removal_count = models.IntegerField(default=0)
    audit_count = models.IntegerField(default=0)
    adhoc_count = models.IntegerField(default=0)
    unsuccessful = models.IntegerField(default=0)
    repair_count = models.IntegerField(default=0)


class AdminDefaults(models.Model):
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    account_admin = models.CharField(max_length=40, blank=True, null=True)
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'city': self.city, 'state': self.state, "account_admin": self.account_admin,
                'zipcodes': self.default_zipcodes.values('zipcode', 'plus_four')}

    def get_location_info(self):
        return {'city': self.city, 'state': self.state,
                'zipcodes': self.default_zipcodes.values('zipcode', 'plus_four')}

    def __unicode__(self):
        return "%s, %s" % (self.city, self.state)

    class Meta:
        verbose_name_plural = "Admin Defaults"


class ZipCodes(models.Model):
    zipcode = models.CharField(max_length=10)
    plus_four = models.CharField(max_length=4, null=True, blank=True)
    defaults = models.ForeignKey(AdminDefaults, related_name='default_zipcodes', blank=True, null=True)

    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'zipcode': self.zipcode, 'plus_four': self.plus_four}

    def __unicode__(self):
        return "%s-%s" % (self.zipcode, self.plus_four)

    class Meta:
        verbose_name_plural = "Zipcodes"


class CartStatus(models.Model):
    LEVEL = (("label-warning", "Warning"), ("label-info", "Info"), ("label-important", "Alert"),
             ("label-success", "Success"), ("label-inverse", "Default"), ('label', 'Inverse'))
    level = models.CharField(max_length=25, choices=LEVEL)
    label = models.CharField(max_length=35)

    #model managers:
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "%s, %s" % (self.level, self.label)

    class Meta:
        verbose_name_plural = "Cart status"


class CartType(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    #model managers:
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        unique_together = (('name', 'size'))
        ordering = ["-name", "-size"]

    def get_info(self):
        return {'name': self.name, 'size': self.size}

    def __unicode__(self):
        return "%s, size: %s" % (self.name, self.size)


class CartParts(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    on_hand = models.IntegerField(blank=True, null=True)

    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name_plural = 'Cart Parts'

    def get_info(self):
        return {'name': self.name, 'on_hand': self.on_hand, 'description': self.description}

    def __unicode__(self):
        return "Part: %s, On Hand: %s" % (self.name, self.on_hand)


class TicketStatus(models.Model):

    LEVEL = (("label-warning", "Warning"), ("label-info", "Info"), ("label-important", "Alert"),
             ("label-success", "Success"), ("label-inverse", "Default"), ('label', 'Inverse'))
    level = models.CharField(max_length=35, choices=LEVEL)
    service_status = models.CharField(max_length=30)

    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "%s, %s" % (self.service_status, self.level)

    class Meta:
        verbose_name_plural = "Ticket Status"


class CartServiceCharge(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50, default='US Dollars')
    description = models.CharField(max_length=120, blank=True)

    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'amount': self.amount, 'description': self.description}

    def __unicode__(self):
        return "Amount: %s, Currency: %s" % (str(self.amount), self.currency)


class CartServiceType(models.Model):
    SERVICE_CODE = (('EX-DEL', 'EX-DEL'), ('EX-REM', 'EX-REM'),
                   ('DEL', 'DEL'), ('REM', 'REM'),
                   ('REPAIR', 'REPAIR'), ('AUDIT', 'AUDIT'))

    service = models.CharField(max_length=25)
    code = models.CharField(max_length=15, choices=SERVICE_CODE)
    description = models.TextField(max_length=300, null=True)
    complete_cart_status_change = models.ForeignKey(CartStatus)
    default_charge = models.ForeignKey(CartServiceCharge, related_name='default_charge', blank=True, null=True)

    #model Managers:
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'service': self.service, 'code': self.code, 'description': self.description}

    def __unicode__(self):
        return "Service: %s, Code: %s" % (self.service, self.code)


class ServiceReasonCodes(models.Model):
    code = models.CharField(max_length=30)
    description = models.TextField(max_length=300, null=True)

    class Meta:
        verbose_name_plural = "Service Reason Codes"

    def __unicode__(self):
        return "Code: %s, Description: %s" % (self.code, self.description)


class Route(models.Model):

    ROUTE_TYPE = (("General", "General"), ("Recycling", "Recycling"),
                  ("Refuse", "Refuse"), ("Yard-Organics", "Yard-Organics"))

    #May turn this into a GeoManaged model for GIS capabilities
    route = models.CharField(max_length=15, null=True)
    route_day = models.CharField(max_length=15, null=True)
    route_type = models.CharField(max_length=20, null=True)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        return {'route': self.route, 'route_day': self.route_day, 'route_type': self.route_type}

    def __unicode__(self):
        return "Route: %s, Day: %s, Route Type: %s" % (self.route, self.route_day, self.route_type)

    class Meta:
        unique_together = (('route', 'route_day', 'route_type'))


class Address(models.Model):
    #Over ride defaults with instance applications.
    CITY = "NA"
    ST = "NA"
    PROPERTY_TYPES = (
                      ('Residential', 'Residential'),
                      ('Business', 'Business'),
                      ('Unoccupied', 'Unoccupied'),
                      ('Vacant Lot', 'Vacant Lot'),
                      ('Multi-Use', 'Multi-Use'),
                     )
    house_number = models.CharField(max_length=8)
    street_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=8, null=True, blank=True)
    direction = models.CharField(max_length=3, null=True, blank=True)
    unit = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=25, default=CITY)
    state = models.CharField(max_length=2, default=ST)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    geocode_status = models.CharField(max_length=20, null=True, blank=True)
    geocode_type = models.CharField(max_length=20, null=True, blank=True)
    property_type = models.CharField(max_length=25, null=True, blank=True,
                                     choices=PROPERTY_TYPES, default=PROPERTY_TYPES[0][0])
    route = models.ManyToManyField(Route, null=True, blank=True)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def _full_street(self):
        full_street = self.street_name

        if self.suffix:
            full_street = full_street + " " + self.suffix

        if self.direction:
            full_street = full_street + " " + self.direction

        return full_street

    full_street = property(_full_street)


    def _full_address(self):
        full_address = "%s %s" % (self.house_number, self.street_name)

        if self.suffix:
            full_address = full_address + " " + self.suffix

        if self.direction:
            full_address = full_address + " " + self.direction

        if self.unit:
            full_address = full_address + " " + self.unit

        return full_address

    full_address = property(_full_address)


    def get_routes(self):
        routes = []
        for route in self.route.all():
            routes.append(route.get_info())
        return routes

    def get_coordinates(self):
        coordinates = {"type": "Feature", "geometry": {"type": "Point", "coordinates":
                       [float(self.latitude or 0), float(self.longitude or 0)]}}
        return coordinates

    def get_absolute_url(self):
        return reverse('location_api_profile', args=[str(self.id)])

    def __unicode__(self):
        return self._full_address()

    class Meta:
        abstract = True
        #Do not want to add a new address that already exist
        unique_together = (('house_number', 'street_name', 'unit', 'direction', 'suffix'))


class CollectionCustomer(models.Model):
    first_name = models.CharField(max_length=25, default="RESIDENT", null=True)
    last_name = models.CharField(max_length=50, default="RESIDENT", null=True)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=75, null=True, blank=True)

    file_upload = models.ForeignKey(CustomersUploadFile, null=True, blank=True, related_name="customers_upload_file")

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

    def get_app_url(self):
        return reverse('customer_app_profile', args=[str(self.id)])

    def get_info(self):
        info = {"id": self.id, "name": self.full_name, "url": self.get_absolute_url()}
        return info


class ForeignSystemCustomerID(models.Model):
    system_name = models.CharField(max_length=25, blank=True, null=True)
    identity = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CollectionCustomer, related_name="customer")
    description = models.TextField(max_length=300, blank=True, null=True)

    #model managers:
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "identity: %s to %s, last updated:%s" % (self.identity, self.system_name, self.last_updated)


class CollectionAddress(Address):
    customer = models.ForeignKey(CollectionCustomer, null=True, blank=True, related_name="customer_location")

    def get_info(self):
        info = {"properties": {"url": self.get_absolute_url(), "id": self.id, "property_type": self.property_type,
                "full_address": self.full_address, "house_number": self.house_number,
                "unit": self.unit, "street_name": self.street_name, "suffix": self.suffix,
                "direction": self.direction, "city": self.city, "state": self.state,
                "zipcode": self.zipcode, "geocode_type": self.geocode_type,
                "geocode_status": self.geocode_status, "carts": self.location.values("id", "serial_number",
                "cart_type__size", "cart_type__name")}, "type": "Feature", "geometry": {"type": "Point", "coordinates":
                [float(self.latitude or 0), float(self.longitude or 0)]}, "routes": self.get_routes()}

        return info


class InventoryAddress(Address):
    contact_number = PhoneNumberField(max_length=15, null=True, blank=True)
    capacity = models.IntegerField()
    description = models.TextField(max_length=300, null=True, blank=True)
    default = models.BooleanField(default=False)

    def get_info(self):
        info = {"properties": {"url": self.get_absolute_url(),"id":self.id, "property_type": self.property_type,
                               "full_address": self.full_address, "house_number": self.house_number,
                               "unit": self.unit, "street_name": self.street_name,
                               "suffix": self.suffix, "direction": self.direction, "city": self.city,
                               "state": self.state, "zipcode": self.zipcode,
                               "geocode_type": self.geocode_type, "geocode_status": self.geocode_status,
                              },"type": "Feature", "geometry":
                    {"type": "Point", "coordinates": [float(self.latitude or 0), float(self.longitude or 0)]},}

        return info

    class Meta:
        verbose_name_plural = "Inventory Address"


class Cart(models.Model):

    """
    CART model stores all cart information.
    These fields are loaded from manufacturing:
    1) Size, 2) Cart Type, 3)RFID, 4) Serial Number, and 5)Born data
    Location comes from Services Center, A & D or from customer delivery services.

    """
    location = models.ForeignKey(CollectionAddress, null=True, blank=True, related_name='location')
    inventory_location = models.ForeignKey(InventoryAddress, null=True, blank=True, related_name="inventory_location")
    at_inventory = models.BooleanField(default=True)
    last_latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    rfid = models.CharField(max_length=30, unique=True)
    serial_number = models.CharField(max_length=30, null=False, blank=False, unique=True)
    current_status = models.ForeignKey(CartStatus, null=True, blank=True,
                                       default=CartStatus.objects.get(label='Inventory'))
    cart_type = models.ForeignKey(CartType, null=True, blank=True, default=1)
    last_updated = models.DateTimeField(auto_now=datetime.now)
    born_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="cart_updated_by_user" )
    file_upload = models.ForeignKey(CartsUploadFile, null=True, blank=True, related_name="cart_upload_file")
    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    report_builder_model_manager = on_site

    def __unicode__(self):
        return "rfid: %s, Type: %s, PK: %s" % (self.rfid, self.cart_type, self.id)

    def get_absolute_url(self):
        return reverse('cart_api_profile', args=[str(self.serial_number)])

    def get_info(self):
        info = {'rfid': self.rfid, "serial": self.serial_number, "id": self.id, "url": self.get_absolute_url(),
                "cart_type__name": self.cart_type.name, "cart_type__size": self.cart_type.size,
                "born_date": self.born_date, "current_status__label": self.current_status.label,
                "current_status__level": self.current_status.level}
        return info

    def save(self, *args, **kwargs):
        current_site = Site.objects.get_current()
        self.site = current_site
        super(Cart, self).save(*args, **kwargs)

class Ticket(models.Model):

    AUDIT_STATUS = (('No Change', 'No Change'), ('Changed', 'Changed'))

    serviced_cart = models.ForeignKey(Cart, null=True, blank=True, related_name='serviced_cart')
    expected_cart = models.ForeignKey(Cart, null=True, blank=True, related_name='expected_cart')

    location = models.ForeignKey(CollectionAddress, related_name="ticket_locations")
    route = models.ForeignKey(Route, related_name='ticket_route', null=True, blank=True)
    service_type = models.ForeignKey(CartServiceType, null=True, blank=True, related_name="service_type")
    cart_type = models.ForeignKey(CartType, null=True, blank=True, related_name="cart_type")
    status = models.ForeignKey(TicketStatus, null=True, blank=True, related_name="status")
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    damaged_parts = models.ManyToManyField(CartParts, null=True, blank=True, related_name="damaged_parts")

    #date information
    date_completed = models.DateTimeField(null=True)
    date_processed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_attempted = models.DateTimeField(auto_now=True, null=True)

    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    device_name = models.CharField(max_length=50, null=True, blank=True)
    success_attempts = models.IntegerField(default=0)
    audit_status = models.CharField(max_length=15, null=True, blank=True, choices=AUDIT_STATUS)
    reason_codes = models.ForeignKey(ServiceReasonCodes, null=True, blank=True)
    processed = models.BooleanField(default=False)
    file_upload = models.ForeignKey(TicketsCompleteUploadFile, null=True, blank=True,
                                    related_name="tickets_upload_file")

    created_by = models.ForeignKey(User, related_name='created_by_user', null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="updated_by_user", null=True, blank=True)


    #model managers
    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        ordering = ["-date_created"]

    def __unicode__(self):
        return "Service Type: %s, Status: %s, Location: %s" % (self.service_type, self.status, self.location)

    def save(self, *args, **kwargs):
        current_site = Site.objects.get_current()
        self.site = current_site
        super(Ticket, self).save(*args, **kwargs)


class TicketComments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200, null=True, blank=True)
    ticket = models.ForeignKey(Ticket, related_name="ticket_comment")
    created_by = models.ForeignKey(User, blank=True, related_name="created_by")

    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_info(self):
        info = {'text': self.text, 'date_created': self.date_created, 'ticket': self.ticket}
        return info


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
        return "%s, %s" % (self.error_date, self.error_message)


class TicketsCompletedUploadFileForm(forms.Form):
    ticket_file = forms.FileField()
    process = forms.BooleanField(label="Process Records", initial=True,  required=False)


class CartsUploadFileForm(forms.Form):
    cart_file = forms.FileField()
    process = forms.BooleanField(label="Process Records", initial=True,  required=False)


class CustomerUploadFileForm(forms.Form):
    customer_file = forms.FileField()
    process = forms.BooleanField(label="Process Records", initial=True, required=False)


class RouteUploadForm(forms.Form):
    route_file = forms.FileField()
    process = forms.BooleanField(label="Process Records", initial=True, required=False)





