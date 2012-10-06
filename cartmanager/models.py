from django.db import models



class Address(models.Model):
    pass


class ServiceCenter(models):
    #service center can also be an A&D service center
    pass

class ServiceCenterAddress(Address):
    pass


class Owner(models):
    pass

class OwnerAddress(Address):
    pass


class CollectionCustomer(models.Model):
    pass

class CollectionAddress(Address):
    ADDRESS_TYPE = (('Billing', 'Billing'), ('Location', 'Location') )
    pass


class Cart(models.Model):
    location = models.ForeignKey(CollectionAddress)


class CartServices(models.Model):
    #Will contain the history as query of closed
    pass

class CartTickets(models.Model):
    pass

class Users(models.Model):
    pass



