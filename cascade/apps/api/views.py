######################################################################################################################
# CartManager API VIEWS: Used to render, create and update content to applications                                   #
######################################################################################################################

import csv
import cStringIO as StringIO

from django.db.models import Q
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponse
from django.utils import simplejson
from django.template import Context, loader

from rest_framework.response import Response as RestResponse
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework import status as django_rest_status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from cascade.libs.renderers import CSVRenderer
from cascade.apps.api.serializers.cartmanager import LocationInfoSerializer, CartSearchSerializer, \
    CartProfileSerializer, CustomerProfileSerializer, CartStatusSerializer, CartTypeSerializer, \
    CartServiceTicketSerializer, AdminLocationDefaultSerializer, UploadFileSerializer, TicketStatusSerializer, \
    TicketCommentSerializer, CartServiceTypeSerializer, RouteSerializer
from cascade.libs.mixins import LoginSiteRequiredMixin
from cascade.apps.cartmanager.models import *


class AdminDefaultLocation(LoginSiteRequiredMixin, APIView):
    model = AdminDefaults
    serializer = AdminLocationDefaultSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get(self, request):
        default_location = AdminDefaults.on_site.get(site=get_current_site(request).id)
        serializer = self.serializer(default_location)
        return RestResponse(serializer.data)


class CartSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    model = Cart
    serializer_class = CartSearchSerializer
    paginate_by = 35
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer, CSVRenderer)

    def get_queryset(self, *args, **kwargs):
        """
        Performs search query for Carts
        """
        search_type = self.request.QUERY_PARAMS.get('type', None)
        value = self.request.QUERY_PARAMS.get('value', None)

        if search_type and value:
            query = Cart.on_site.filter()
            value = value.strip()
            if search_type == 'address':
                address = value.split(' ')
                if len(address) == 1:
                    #address only contains street name
                    street_name = address[0].strip().upper()
                    query = Cart.on_site.filter(location__street_name__startswith=street_name)
                else:
                    house_number = address[0].strip().upper()
                    street_name = address[1].strip().upper()
                    query = query.filter(location__street_name__startswith=street_name,
                                         location__house_number=house_number)
                    if query.count() == 0:
                        #look for non exact
                        query = Cart.on_site.filter(location__street_name__contains=street_name,
                                                    location__house_number__contains=house_number)
            elif search_type == 'serial_number':
                query = query.filter(serial_number__contains=str(value))
            elif search_type == 'type':
                query = query.filter(cart_type__name=value)
            elif search_type == 'size':
                print value
                query = query.filter(cart_type__size=int(value))
            elif search_type == 'status':
                query = query.filter(current_status__label=value)
            else:
                raise Http404
            return query

    def list(self, request, *args, **kwargs):

        search_type = self.request.QUERY_PARAMS.get('type', None)
        value = self.request.QUERY_PARAMS.get('value', None)

        if search_type and value:
            return super(CartSearchAPI, self).list(request, *args, **kwargs)
        else:
            return RestResponse({"detail": "No Search values received or incorrect values received...try again. "},
                                status=django_rest_status.HTTP_404_NOT_FOUND)


class TicketSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    model = Ticket
    serializer_class = CartServiceTicketSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer, JSONPRenderer, BrowsableAPIRenderer, CSVRenderer)
    paginate_by = 100

    def get_queryset(self):
        cart_serial = self.request.QUERY_PARAMS.get('serial_number', None)
        customer_id = self.request.QUERY_PARAMS.get("customer_id", None)
        cart_size = self.request.QUERY_PARAMS.get('cart_size', 'ALL')
        cart_type = self.request.QUERY_PARAMS.get('cart_type', 'ALL')
        service_status = self.request.QUERY_PARAMS.get('status', 'ALL')
        service_type = self.request.QUERY_PARAMS.get('service', 'ALL')
        processed = self.request.QUERY_PARAMS.get('processed', 'True')
        route_type = self.request.QUERY_PARAMS.get('route_type', 'ALL')
        route_day = self.request.QUERY_PARAMS.get('route_day', 'ALL')
        route = self.request.QUERY_PARAMS.get('route', 'ALL')

        sort_by = self.request.QUERY_PARAMS.get('sort_by', None)
        page_size = self.request.QUERY_PARAMS.get('page_size', None)

        try:
            if page_size:
                self.paginate_by = page_size

            if sort_by:
                query = Ticket.on_site.order_by(sort_by)
            else:
                query = Ticket.on_site.all()

            if cart_serial:
                query = query.filter(
                    Q(expected_cart__serial_number=cart_serial) | Q(serviced_cart__serial_number=cart_serial))
            if customer_id:
                customer = CollectionCustomer.on_site.get(pk=customer_id)
                #get all tickets where the location is equal to a customers location
                locations = customer.customer_location.all()
                query = query.filter(location__in=locations)
            if service_status != 'ALL':
                query = query.filter(status__service_status=service_status)
            if cart_type != 'ALL':
                query = query.filter(cart_type__name=cart_type)
            if cart_size != 'ALL':
                query = query.filter(cart_type__size=cart_size)
            if service_type != 'ALL':
                query = query.filter(service_type__service=service_type)
            if processed == 'False':
                query = query.filter(processed=False)
            if route_day != 'ALL':
                routes = Route.on_site.filter(route_day=route_day)
                query = query.filter(route__in=routes)
            if route_type != 'ALL':
                routes = Route.on_site.filter(route_type=route_type)
                query = query.filter(route__in=routes)
            if route != 'ALL':
                route = Route.on_site.filter(route=route)
                query = query.filter(route=route)

            #get only the distinct tickets

            return query
        except:
            raise Http404

    def csv_out(self, row, index):
        csvfile = StringIO.StringIO()
        csv_writer = csv.writer(csvfile)
        if index == 1:
            csv_writer.writerow(
                ['SystemID', 'StreetName', 'HouseNumber', 'UnitNumber', 'ServiceType', 'RFID', 'CartSize', 'CartType'])
        csv_writer.writerow(
            [row.id, row.location.street_name, row.location.house_number, row.location.unit, row.service_type.code,
             str(getattr(row.expected_cart, 'rfid', '')) + '"', row.cart_type.size, row.cart_type])
        return csvfile.getvalue()

    def stream_response_generator(self, data):
        index = 0
        for row in data:
            index += 1
            yield self.csv_out(row, index)
            #time.sleep(0.09)

    def list(self, request, *args, **kwargs):
        if self.request.accepted_renderer.format == "csv":
            file_name = self.request.QUERY_PARAMS.get('file_name', 'cart_logic_%s' % str(datetime.now().isoformat()))
            data = self.get_queryset()
            response = HttpResponse(self.stream_response_generator(data), mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s.csv' % file_name
            return response
        return super(TicketSearchAPI, self).list(request, *args, **kwargs)


class LocationAPI(LoginSiteRequiredMixin, APIView):
    model = CollectionAddress
    serializer = LocationInfoSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer, CSVRenderer, JSONPRenderer, BrowsableAPIRenderer,)

    def get_object(self, location_id):
        try:
            return CollectionAddress.on_site.get(id=location_id)
        except CollectionAddress.DoesNotExist:
            raise Http404

    def get(self, request, location_id, *args, **kwargs):
        location = self.get_object(location_id)
        serializer = self.serializer(location)
        return RestResponse(serializer.data)

    def post(self, request, location_id, *args, **kwargs):
        json_data = simplejson.loads(request.raw_post_data)
        operation = json_data.get('operation', None)
        customer_id = json_data.get('customer_id', None)

        if customer_id:
            customer = CollectionCustomer.on_site.get(id=customer_id)
            if location_id == 'New':
                route_list = json_data.get('routes', None)
                house_number = json_data.get('house_number', None)
                street_name = json_data.get('street_name', None)
                unit = json_data.get('unit', None)
                zipcode = json_data.get('zipcode', None)
                property_type = json_data.get('property_type', None)
                city = json_data.get('city', None)
                state = json_data.get('state', None)
                latitude = json_data.get('latitude', None)
                longitude = json_data.get('longitude', None)
                geocode_status = json_data.get('geocode_status', None)
                location = CollectionAddress(site=get_current_site(self.request), house_number=house_number.strip(),
                                             street_name=street_name.strip().upper(),
                                             unit=unit, zipcode=zipcode, property_type=property_type, city=city,
                                             state=state, latitude=latitude, longitude=longitude,
                                             geocode_status=geocode_status, customer=customer)
                location.save()

                #add routes
                if route_list:
                    routes = simplejson.loads(route_list)
                    for route in routes:
                        add_route = Route.on_site.get(route=route['route'],
                                                      route_type=route['route_type'],
                                                      route_day=route['route_day'])
                        location.route.add(add_route)
                    location.save()

                return RestResponse({'details': {'message': "Saved new address: %s  for customer: %s" %
                                                            (location, customer._get_full_name()),
                                                 'message_type': 'Success'}},
                                    status=django_rest_status.HTTP_200_OK)
            else:
                location = self.get_object(location_id)
                if operation == 'remove':
                #Make sure the customer is currently assigned to the address
                    if location.customer == customer:
                        location.customer = None
                        location.save()
                        return RestResponse({'details': {
                            'message': "Removed address: %s  for customer: %s" % (location, customer._get_full_name()),
                            'message_type': 'Success'}}, status=django_rest_status.HTTP_200_OK)
                    else:
                        return RestResponse({'details': {
                            'message': "Address: %s  does not have customer: %s" % (
                                location, customer._get_full_name()),
                            'message_type': 'Failed'}}, status=django_rest_status.HTTP_200_OK)
                elif operation == 'change':
                    current_customer = location.customer
                    location.customer = customer
                    location.save()
                    return RestResponse({'details': {'message': "Changed address: %s  from: %s to: %s" %
                                       (location, current_customer._get_full_name(), customer._get_full_name()),
                                        'message_type': 'Success'}}, status=django_rest_status.HTTP_200_OK)
                elif operation:
                    return RestResponse({'details': {'message': "No operation value given", 'message_type': 'Failed'}},
                                        status=django_rest_status.HTTP_200_OK)
        else:
            return RestResponse({'details': {'message': "No customer information received", 'message_type': 'Failed'}},
                                status=django_rest_status.HTTP_200_OK)


class LocationSearchAPI(LoginSiteRequiredMixin, APIView):
    def get_queryset(self, address, address_id, customer_id):
        try:
            if address:
                house_number = address.split(' ')[0].strip().upper()
                street_name = address.split(house_number)[1].strip().upper()
                query = CollectionAddress.on_site.filter(house_number=house_number, street_name__contains=street_name)
                return query
            elif address_id:
                query = CollectionAddress.on_site.get(id=address_id)
                return query
            elif customer_id:
                customer = CollectionCustomer.on_site.get(id=customer_id)
                query = CollectionAddress.on_site.filter(customer=customer)
                return query
            else:
                raise Http404
        except:
            raise Http404

    def get(self, request, format=None):
        address = self.request.QUERY_PARAMS.get('address', None)
        address_id = self.request.QUERY_PARAMS.get('address_id', None)
        customer_id = self.request.QUERY_PARAMS.get('customer_id', None)
        addresses = self.get_queryset(address, address_id, customer_id)
        serializer = LocationInfoSerializer(addresses)
        return RestResponse(serializer.data)


class CartProfileAPI(LoginSiteRequiredMixin, APIView):
    model = Cart
    serializer_class = CartProfileSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, serial_number):
        try:
            return Cart.on_site.get(serial_number=serial_number)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, serial_number, format=None):
        cart = self.get_object(serial_number)
        serializer = CartProfileSerializer(cart)

        if request.accepted_renderer.format == 'csv':
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=profile.csv'
            t = loader.get_template('profile.csv')
            c = Context({'data': cart}, )
            response.write(t.render(c))
            return response

        return RestResponse(serializer.data)

    def post(self, request, serial_number):

        try:
            json_data = simplejson.loads(request.raw_post_data)
            create_new = json_data.get('create_new', None)
             #grabbing values to be updated or None
            cart_type_name = json_data.get('cart_type__name', None)
            cart_type_size = json_data.get('cart_type__size', None)
            current_status_id = json_data.get('current_status', None)
            location_id = json_data.get('location_id', None)
            latitude = json_data.get('latitude', None)
            longitude = json_data.get('longitude', None)

            if create_new:
                #if new cart flag then add new cart to inventory
                cart = Cart()
                cart.serial_number = serial_number
                rfid = json_data.get('rfid', None)

                if rfid:
                    cart.rfid = rfid
                else:
                    cart.rfid = serial_number
                cart.at_inventory = True
                born_date = json_data.get('born_date', None)
                if born_date:
                    converted_date = datetime.strptime(born_date, '%m-%d-%Y')
                    cart.born_date = converted_date
                cart.current_status = CartStatus.objects.get(label='Inventory')
                cart.inventory_location = InventoryAddress.objects.get(default=True)

            else:
                cart = self.get_object(serial_number)
            #check for cart type and save to cart, if None then no value given skip it
            if cart_type_name and cart_type_size:
                print cart_type_name
                cart.cart_type = CartType.objects.get(name=cart_type_name, size=cart_type_size)

            #check for location and update latitude + longitude to collection address lat and long
            if location_id:
                cart.location = CollectionAddress.objects.get(pk=location_id)
                cart.last_latitude = cart.location.latitude
                cart.last_longitude = cart.location.longitude

            #check for current status
            if current_status_id:
                cart.current_status = CartStatus.objects.get(pk=current_status_id)

            #check for latitude and longitude (map moves)
            if latitude and longitude:
                cart.last_latitude = latitude
                cart.last_longitude = longitude
            cart.updated_by = request.user
            cart.save()

            return RestResponse({"details": {'message': "Update complete for %s " % serial_number,
                                             'message_type': 'Success', "time": datetime.now()}},
                                status=django_rest_status.HTTP_200_OK)
        except Exception as e:
            return RestResponse(
                {"details": {'message': "The cart did not save or update, Error: %s" % e,
                             'message_type': 'Failed', "time": datetime.now()}}, status=django_rest_status.HTTP_200_OK)


class TicketAPI(LoginSiteRequiredMixin, APIView):
    model = Ticket
    serializer_class = CartServiceTicketSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, ticket_id):
        try:
            ticket = Ticket.on_site.get(id=ticket_id)
            return ticket

        except ObjectDoesNotExist:
            return None

    def get(self, request, ticket_id, format=None):
        try:
            ticket = self.get_object(ticket_id)
            if ticket:
                serializer = CartServiceTicketSerializer(ticket)
                return RestResponse(serializer.data)
            else:
                return RestResponse({"details": {
                                     "message": "Sorry! did not find ticket with id: '%s. Did it get deleted?'" % (
                                                ticket_id), 'message_type': 'Failed'},
                                     "time": datetime.now()}, status=django_rest_status.HTTP_200_OK)
        except ValueError:
            #except ValueError if ticket_id is not an number
            RestResponse({"details": {'message': "Sorry! ticket ids are numbers, not ...'%s!'" % (ticket_id),
                          'message_type': 'Failed'},
                          "time": datetime.now()}, status=django_rest_status.HTTP_200_OK)

    def post(self, request, ticket_id, format=None):
        json_data = simplejson.loads(request.body)

        if ticket_id == 'New':

            try:
                location_id = json_data.get('location_id', None)
                house_number = json_data.get('house_number', None)
                street_name = json_data.get('street_name', None)
                unit = json_data.get('address_unit', None)

                #excepts both location id and address for the Collection Address
                #client built for address information, we want this flexibility as I may not know the address_id
                if location_id:
                    location = CollectionAddress.on_site.get(pk=location_id)
                #else try to get the house number and street name
                elif house_number and street_name:
                    #check for a unit (i.e. apartment or condo)
                    if unit:
                        location = CollectionAddress.on_site.get(house_number=house_number, street_name=street_name,
                                                                 unit=unit)
                    else:
                        #ok no unit so just get the address using the house number and street name
                        location = CollectionAddress.on_site.get(house_number=house_number, street_name=street_name)

                else:
                    return RestResponse({"details": {'message': "No address information given",
                                        'message_type': 'Failed'},
                                        "time": datetime.now()}, status=django_rest_status.HTTP_200_OK)

                #Get the current service type and a cart service status object of requested
                requested_service_type = json_data.get('service_type', None)
                requested_ticket_status = TicketStatus.on_site.get(service_status='Requested')
                expected_cart_serial_number = json_data.get('cart_serial_number', None)
                size = json_data.get('cart_size', None)
                cart_type_name = json_data.get('cart_type', None)

                #get the locations route to assign to a ticket
                try:
                    route = Route.objects.get(collectionaddress=location, route_type=cart_type_name)
                except ObjectDoesNotExist:
                    route = None

                #If we have an expected cart serial number it is a remove, exchange, repair or audit
                #TODO put repair or audits in here
                if expected_cart_serial_number:
                    expected_cart = Cart.on_site.get(serial_number=expected_cart_serial_number)
                    if requested_service_type == 'Exchange' or 'Remove':
                        if requested_service_type == 'Exchange':
                            service_type_remove = CartServiceType.on_site.get(code='EX-REM')
                        else:
                            service_type_remove = CartServiceType.on_site.get(code='REM')

                        remove_ticket = Ticket(created_by=request.user, location=location,
                                               status=requested_ticket_status,
                                               expected_cart=expected_cart,
                                               service_type=service_type_remove,
                                               cart_type=expected_cart.cart_type)

                        if route:
                            remove_ticket.route = route

                        remove_ticket.save()

                #Create service ticket or tickets below, some code repeated but feels more readable

                if requested_service_type == 'Delivery':
                    #Delivery? You should get and add the cart type from cart type name and size
                    #Create a new delivery ticket service type of code DEL.
                    service_type = CartServiceType.on_site.get(code='DEL')
                    cart_type = CartType.on_site.get(name=cart_type_name, size=size)
                    delivery_ticket = Ticket(created_by=request.user, location=location, service_type=service_type,
                                             status=requested_ticket_status,
                                             cart_type=cart_type)

                    if route:
                        delivery_ticket.route = route

                    delivery_ticket.save()

                elif requested_service_type == 'Exchange':
                    #Exchange? You should get and add the cart type from name and size
                    #Create a new delivery ticket with service type EX-DEL and remove ticket with service type EX-REM,
                    service_type = CartServiceType.on_site.get(code='EX-DEL')
                    cart_type = CartType.on_site.get(name=cart_type_name, size=size)
                    exchange_del_ticket = Ticket(created_by=request.user, location=location, service_type=service_type,
                                                 status=requested_ticket_status,
                                                 cart_type=cart_type)
                    if route:
                        exchange_del_ticket.route = route

                    exchange_del_ticket.save()
                return RestResponse({'details': {
                    'message': 'Success! New %s Ticket(s) created for %s' % (requested_service_type, location),
                    'message_type': 'Success'}}, status=django_rest_status.HTTP_201_CREATED)

            except Exception as e:
                return RestResponse({'details': {'message': "Sorry! ticket could not be created, code: %s" % e,
                                                 'message_type': 'Failed'}},
                                    status=django_rest_status.HTTP_200_OK)

        else:
            #Expecting this to be a status change if it is not New
            #Change status of the ticket id & process the cart changes
            try:
                ticket = self.get_object(ticket_id)
                update_status = json_data.get('status', None)
                ticket.updated_by = request.user
                #updated success_attempts no matter what the service type iss
                ticket.success_attempts = ticket.success_attempts + 1

                if update_status == 'Completed':
                #get the serviced_cart_serial_number
                    serial_number = json_data.get('serial_number', None)
                    try:
                        cart = Cart.on_site.get(serial_number=serial_number)
                    except Cart.DoesNotExist as e:
                        return RestResponse({'details': {'message':
                                                             'Could not find  a cart with serial number: %s' % serial_number,
                                                         'message_type': 'Fail'}},
                                            status=django_rest_status.HTTP_200_OK)
                    status = TicketStatus.on_site.get(service_status=update_status)
                    #change the carts current status to the tickets service type complete status map
                    cart.current_status = ticket.service_type.complete_cart_status_change
                    #TODO Check that the ticket has not already been completed

                    #Update the Ticket
                    ticket.status = status
                    ticket.serviced_cart = cart
                    ticket.processed = True
                    ticket.date_completed = datetime.now()
                    #Update the Cart
                    if ticket.service_type.code == 'DEL' or ticket.service_type.code == 'EX-DEL':
                        cart.location = ticket.location
                    elif ticket.service_type.code == "EX-REM" or ticket.service_type.code == "REM":
                        cart.location = None
                        cart.at_inventory = True
                        cart.inventory_location = InventoryAddress.on_site.get(default=True)

                    cart.save()
                ticket.save()
                return RestResponse({'details': {'message': 'Ticket: %s has been updated' % ticket_id,

                                                 'message_type': 'Success'}},
                                    status=django_rest_status.HTTP_200_OK)

            except ValueError as e:
                #TODO beef up the error response ...to generic
                return RestResponse(
                    {'details': {'message': "Sorry! ticket could not be updated: %s" % e, 'message_type': 'Failed'}},
                    status=django_rest_status.HTTP_200_OK)

    def delete(self, request, ticket_id, format=None):
        ticket = self.get_object(ticket_id)
        ticket.delete()
        return RestResponse({'details': {'message': "Ticket %s Deleted" % ticket_id, 'message_type': 'Success'}},
                            status=django_rest_status.HTTP_200_OK)


class TicketCommentAPI(APIView):
    model = TicketComments
    serializer_class = TicketCommentSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, ticket_id):
        try:
            return TicketComments.on_site.filter(ticket=ticket_id)
        except TicketComments.DoesNotExist:
            return False

    def get(self, request, ticket_id, format=None):
        comments = self.get_object(ticket_id)
        if comments:
            serializer = TicketCommentSerializer(comments)
            return RestResponse(serializer.data)
        else:
            return RestResponse({'details': {'message': 'Nothing to say...', 'count': 0, 'message_type': 'Success'}},
                                status=django_rest_status.HTTP_200_OK)

    def post(self, request, ticket_id, format=None):

        json_data = simplejson.loads(request.body)
        comment = json_data.get('text', None)
        ticket = Ticket.on_site.get(pk=ticket_id)

        if comment:
            new_comment = TicketComments(site=get_current_site(self.request), text=comment, ticket=ticket,
                                         created_by=self.request.user)
            new_comment.save()

            return RestResponse(
                {'details': {'message': "Comment Saved", 'message_type': 'Success', 'comment_id': new_comment.id}},
                status=django_rest_status.HTTP_200_OK)
        else:
            return RestResponse({'details': {'message': "No text given", 'message_type': 'Failed'}},
                                status=django_rest_status.HTTP_200_OK)

    def delete(self, request, ticket_id, format=None):
        json_data = simplejson.loads(request.body)
        comment_id = json_data.get('comment_id', None)
        try:
            comment = TicketComments.on_site.get(pk=comment_id)
            if comment.created_by == request.user:
                comment.delete()
                return RestResponse({'details': {'message': "Comment has been deleted", 'message_type': 'Success'}},
                                    status=django_rest_status.HTTP_200_OK)
        except TicketComments.DoesNotExist:
            return RestResponse({'details': {'message': "Comment Does not exist", 'message_type': 'Failed'}},
                                status=django_rest_status.HTTP_200_OK)


class CustomerProfileAPI(APIView, LoginSiteRequiredMixin):
    model = CollectionCustomer
    serializer_class = CustomerProfileSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, customer_id):
        try:
            return CollectionCustomer.on_site.get(id=customer_id)
        except CollectionCustomer.DoesNotExist:
            raise Http404

    def get(self, request, customer_id, format=None):
        customer = self.get_object(customer_id)
        serializer = CustomerProfileSerializer(customer)
        return RestResponse(serializer.data)

    def post(self, request, customer_id, format=None):
        json_data = simplejson.loads(request.raw_post_data)
        first_name = json_data.get('first_name', None)
        last_name = json_data.get('last_name', None)
        phone_number = json_data.get('phone_number', None)
        email = json_data.get('email', None)

        if customer_id == 'New':
            customer = CollectionCustomer()
            customer.site = get_current_site(self.request)
        else:
            customer = self.get_object(customer_id)

        if first_name and last_name and phone_number:
            customer.first_name = first_name.upper()
            customer.last_name = last_name.upper()
            customer.email = email.upper()
            customer.phone_number = phone_number
            customer.save()
            return RestResponse({"details": {"message": "Changes saved for customer: %s" % (customer._get_full_name()),
                                             "customer_id": customer.id, "message_type": "Success"}},
                                status=django_rest_status.HTTP_200_OK)
        else:
            return RestResponse({'details': {'message': "Missing one or more values", 'message_type': 'Failed'}},
                                status=django_rest_status.HTTP_200_OK)


class CartStatusAPI(ListAPIView):
    model = CartStatus
    serializer_class = CartStatusSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        return CartStatus.on_site.all()


class TicketStatusAPI(ListAPIView):
    model = TicketStatus
    serializer_class = TicketStatusSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        return TicketStatus.on_site.all()


class TicketServiceTypeAPI(ListAPIView):
    model = CartServiceType
    serializer_class = CartServiceTypeSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        return CartServiceType.on_site.all()


class CartTypeAPI(LoginSiteRequiredMixin, ListAPIView):
    model = CartType
    serializer = CartTypeSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_queryset(self):
        size = self.request.QUERY_PARAMS.get('size', None)
        if size:
            queryset = CartType.on_site.filter(size=size)
            return queryset
        else:
            queryset = CartType.on_site.all()
            return queryset


class FileUploadListAPI(LoginSiteRequiredMixin, ListAPIView):
    serializer_class = UploadFileSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)
    paginate_by = 100

    def get_queryset(self):

        file_query = None
        file_type = self.request.QUERY_PARAMS.get('file_type', None)
        status = self.request.QUERY_PARAMS.get('file_status', None)
        file_id = self.request.QUERY_PARAMS.get('file_id', None)
        sort_by = self.request.QUERY_PARAMS.get('sort_by', None)
        page_size = self.request.QUERY_PARAMS.get('page_size', None)

        if page_size:
            self.paginate_by = page_size
        if file_type == 'Carts':
            file_query = CartsUploadFile.on_site.all()
        elif file_type == 'Tickets':
            file_query = TicketsCompleteUploadFile.on_site.all()
        elif file_type == 'Customers':
            file_query = CustomersUploadFile.on_site.all()
        elif file_type == 'Route':
            file_query = RouteUploadFile.on_site.all()
        if file_query and status:
            if status.upper() != 'ALL':
                file_query = file_query.filter(status=status.upper())
        if file_query and sort_by:
            file_query = file_query.order_by(sort_by)
        if file_id:
            file_query = file_query.filter(pk=file_id)
        if file_query:
            return file_query
        else:
            raise Http404


class RouteListAPI(LoginSiteRequiredMixin, ListAPIView):
    """
    Provides search api for routes
    """
    serializer_class = RouteSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)
    paginate_by = 100

    def get_queryset(self):
        route = self.request.QUERY_PARAMS.get('route', 'ALL')
        route_day = self.request.QUERY_PARAMS.get('route_day', 'ALL')
        route_type = self.request.QUERY_PARAMS.get('route_type', 'ALL')

        file_query = Route.on_site.all()

        if route.upper() != 'ALL':
            file_query = file_query.filter(route=route)

        if route_day.upper() != 'ALL':
            file_query = file_query.filter(route_day=route_day)

        if route_type.upper() != 'ALL':
            file_query = file_query.filter(route_type=route_type)

        return file_query



