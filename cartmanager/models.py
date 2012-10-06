from django.db import models
from django.db.models.deletion import DO_NOTHING


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
    CART model stores all cart information. All the physical characteristics are loaded into
    the database from the manufacturing system.
    """

    CART_TYPE = (('Recycle', 'Recycle'), ('Refuse', 'Refuse'), ('Yard Waste', 'Yard Waste'), ('Other','Other') )
    CART_SIZE = ((35, 35), (64, 64), (96, 96))
    owner = models.OneToOneField(Owner, on_delete=DO_NOTHING, to_field='customer_number')
    location = models.ForeignKey(CollectionAddress)
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



