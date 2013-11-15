__author__ = 'jbennett'
from cascade.apps.cartmanager.models import Cart, Ticket, TicketComments, CollectionCustomer, \
    CollectionAddress, Route, DataErrors, CustomersUploadFile, \
    CartsUploadFile, TicketsCompleteUploadFile, RouteUploadFile


class RemoveData:

    def remove_carts(self):
        carts = Cart.objects.all()
        print "Deleting: %s carts" % carts.count()
        carts.delete()

    def remove_customer(self):
        customers = CollectionCustomer.objects.all()
        print "Deleting: %s customers" % customers.count()
        customers.delete()

    def remove_tickets(self):
        tickets = Ticket.objects.all()
        print "Deleting: %s tickets" % tickets.count()
        tickets.delete()

    def remove_addresses(self):
        addresses = CollectionAddress.objects.all()
        print "Deleting: %s addresses" % addresses.count()
        addresses.delete()

    def remove_ticket_comments(self):
        ticket_comments = TicketComments.objects.all()
        print "Deleting: %s tickets comments" % ticket_comments.count()
        ticket_comments.delete()

    def remove_routes(self):
        routes = Route.objects.all()
        print "Deleting: %s routes" % routes.count()
        routes.delete()

    def remove_data_error(self):
        data_error = DataErrors.objects.all()
        print "Deleting: %s routes" % data_error.count()
        data_error.delete()

    def remove_uploaded_files(self):
        c = CustomersUploadFile.objects.all()
        t = TicketsCompleteUploadFile.objects.all()
        r = RouteUploadFile.objects.all()
        ca = CartsUploadFile.objects.all()
        print "Deleting %s customer, %s tickets, %s routes, %s and cart upload files" % (c.count(),
                                                                                         t.count(), r.count(),
                                                                                         ca.count())

    def remove_all(self):
        self.remove_carts()
        self.remove_customer()
        self.remove_ticket_comments()
        self.remove_tickets()
        self.remove_addresses()
        self.remove_routes()
