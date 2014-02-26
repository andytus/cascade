__author__ = 'jbennett'
from cascade.apps.cartmanager.models import Cart, Ticket, TicketComments, CollectionCustomer, \
    CollectionAddress, Route, DataErrors, CustomersUploadFile, \
    CartsUploadFile, TicketsCompleteUploadFile, RouteUploadFile, ZipCodes, AdminDefaults

from django.contrib.sites.models import Site


class RemoveData:

    def __init__(self, site):
        self.site = Site.objects.get(pk=site)

    def remove_carts(self):
        carts = Cart.objects.filter(site=self.site)
        print "Deleting: %s carts" % carts.count()
        carts.delete()

    def remove_customer(self):
        customers = CollectionCustomer.objects.filter(site=self.site)
        print "Deleting: %s customers" % customers.count()
        customers.delete()

    def remove_tickets(self):
        tickets = Ticket.objects.filter(site=self.site)
        print "Deleting: %s tickets" % tickets.count()
        tickets.delete()

    def remove_addresses(self):
        addresses = CollectionAddress.objects.filter(site=self.site)
        print "Deleting: %s addresses" % addresses.count()
        addresses.delete()

    def remove_ticket_comments(self):
        ticket_comments = TicketComments.objects.filter(site=self.site)
        print "Deleting: %s tickets comments" % ticket_comments.count()
        ticket_comments.delete()

    def remove_routes(self):
        routes = Route.objects.filter(site=self.site)
        print "Deleting: %s routes" % routes.count()
        routes.delete()

    def remove_data_error(self):
        data_error = DataErrors.objects.filter(site=self.site)
        print "Deleting: %s data errors" % data_error.count()
        data_error.delete()

    def remove_uploaded_files(self):
        c = CustomersUploadFile.objects.filter(site=self.site)
        t = TicketsCompleteUploadFile.objects.filter(site=self.site)
        r = RouteUploadFile.objects.filter(site=self.site)
        ca = CartsUploadFile.objects.filter(site=self.site)
        print "Deleting %s customer, %s tickets, %s routes, %s and cart upload files" % (c.count(),
                                                                                         t.count(), r.count(),
                                                                                          ca.count())
        c.delete()
        t.delete()
        r.delete()
        ca.delete()

    def remove_zipcodes(self):
        z = ZipCodes.objects.filter(site=self.site)
        print "Deleting: %s zipcodes" % z.count()
        z.delete()

    def remove_admin_defaults(self):
        a = AdminDefaults.objects.filter(site=self.site)
        print "Removing AdminDefaults"
        a.delete()


    def remove_all(self):
        self.remove_carts()
        self.remove_customer()
        self.remove_ticket_comments()
        self.remove_tickets()
        self.remove_addresses()
        self.remove_routes()
