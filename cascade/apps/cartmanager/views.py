from datetime import datetime
from django.shortcuts import  render
from django.utils import simplejson
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from cascade.apps.cartmanager.models import *
from django.template import loader, Context
from django.views.generic import FormView, TemplateView, ListView
from django.http import Http404
from django.http import HttpResponse
from rest_framework import status as django_rest_status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, MultipleObjectAPIView
from rest_framework.mixins import  RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response as RestResponse
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from cascade.libs.renderers import CSVRenderer
from django.db.models import Q
from django_rq import enqueue
from cascade.libs.uploads import process_upload_records

from cascade.apps.cartmanager.serializer import LocationInfoSerializer, CartSearchSerializer, CartProfileSerializer,\
    CustomerProfileSerializer, AddressCartProfileSerializer,\
    CartStatusSerializer, CartTypeSerializer, CartServiceTicketSerializer, AdminLocationDefaultSerializer,  \
    CustomerInfoSerializer, CartsUploadFileSerializer, TicketStatusSerializer, TicketCommentSerializer, \
    CartServiceTypeSerializer
from cascade.libs.mixins import LoginSiteRequiredMixin


class CartSearch(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_search.html'
    search_query = None

    def get_context_data(self, **kwargs):
        context = super(CartSearch, self).get_context_data(**kwargs)
        #TODO Create a default search query ... selecting the last 50 modified and remove the raise
        search_parameters = self.request.GET.get('search_query', None)
        if search_parameters:
            context['search_parameters'] = self.request.GET['search_query']
        return context


class CartAddressChange(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_profile_address_change.html'

    def get_context_data(self, **kwargs):
        context = super(CartAddressChange, self).get_context_data(**kwargs)
        #putting in for duplicate cart serials, not used right now
        if kwargs['serial_number']:
            context['serial_number'] = kwargs['serial_number']
        else:
            raise Http404
        return context

class CartProfile(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_profile.html'

    def get_context_data(self, **kwargs):
        context = super(CartProfile, self).get_context_data(**kwargs)
        if kwargs['serial_number']:
            context['serial_number'] = kwargs['serial_number']
        else:
            raise Http404
        return context


class CartProfileMap(CartProfile):
    template_name = 'cart_profile_map.html'


class CartReport(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_report.html'


class LocationSearch(LoginSiteRequiredMixin, TemplateView):
    template_name = 'location_search.html'

    def get_context_data(self, **kwargs):
        context = super(LocationSearch, self).get_context_data(**kwargs)
        context['address_id'] = self.request.GET.get('address_id', None)
        return context



class CustomerProfile(LoginSiteRequiredMixin, TemplateView):
    template_name ='customer_profile.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerProfile, self).get_context_data()
        if kwargs["customer_id"]:
            context['customer_id'] = kwargs["customer_id"]
        else:
            raise Http404
        return context


class CustomerNew(LoginSiteRequiredMixin, TemplateView):
    template_name = 'customer_new.html'




class CustomerReport(LoginSiteRequiredMixin, TemplateView):
    template_name = 'customer_report.html'


class TicketReport(LoginSiteRequiredMixin, TemplateView):
    template_name = 'ticket_report.html'


class TicketNew(LoginSiteRequiredMixin, TemplateView):
    template_name = "ticket_new.html"

    def get_context_data(self, **kwargs):
        context = super(TicketNew, self).get_context_data(**kwargs)

        if kwargs['ticket_id']:
            context['ticket_id'] = kwargs['ticket_id']

            if kwargs['ticket_id'] == 'New':
                # get parameters for call to back to AJAX or None
                # None will mean we need to get them from the user before pushing
                # data to the new ticket api
                location_id = self.request.GET.get('location_id', None)

                if location_id:
                    #Just sending back the location id, the client can look up the address info using the API
                    #only needed for deliveries can get location id from cart for other request
                    context['location_id'] = location_id


                cart_id = self.request.GET.get('cart_id', None)
                #TODO change to serial number
                if cart_id:
                    #send over the cart id to use in the Ticket API and the cart serial for user verification.
                    #Note: should use cart serial but currently can not be trusted as unique for each account
                    cart = Cart.on_site.get(pk=cart_id)
                    context['cart_id'] = cart_id
                    context['serial_number'] = cart.serial_number
                    # check for a location else use inventory location
                    if cart.location:
                        context['cart_address_house_number'] = cart.location.house_number
                        context['cart_address_street_name'] = cart.location.street_name
                        if cart.location.unit:
                            context['cart_address_unit'] = cart.location.unit
        else:
            raise Http404
        return context



class TicketProfile(LoginSiteRequiredMixin, TemplateView):
    template_name = "ticket_profile.html"

    def get_context_data(self, **kwargs):
        context = super(TicketProfile, self).get_context_data(**kwargs)
        if kwargs['ticket_id']:
            context['ticket_id'] = kwargs['ticket_id']
        else:
            raise Http404
        return context




######################################################################################################################
#API VIEWS: Used to render, create and update content to applications                                                #
######################################################################################################################

class AdminDefaultLocation(LoginSiteRequiredMixin, APIView):
    model = AdminDefaults
    serializer = AdminLocationDefaultSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get(self, request):
        print get_current_site(request).id
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
                house_number = value.split(' ')[0].strip().upper()
                street_name = value.split(house_number)[1].strip().upper()
                print house_number, street_name
                query = query.filter(location__street_name=street_name, location__house_number=house_number)
            elif search_type == 'serial_number':
                query = query.filter(serial_number__contains=str(value))
            elif search_type == 'type':
                query = query.filter(cart_type__name=value)
            elif  search_type == 'size':
                query = query.filter(size=value)
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
            return RestResponse({"detail":"No Search values received or incorrect values received...try again. "}, status=django_rest_status.HTTP_404_NOT_FOUND)



class TicketSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    model = Ticket
    serializer_class = CartServiceTicketSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer, CSVRenderer, JSONPRenderer, BrowsableAPIRenderer,)
    paginate_by = 100


    def get_queryset(self):
        search_by = simplejson.loads(self.request.QUERY_PARAMS.get('search_by', None))
        if search_by:
            cart_serial = search_by.get('serial_number', None)
            customer_id = search_by.get("customer_id", None)
            cart_size = search_by.get('cart_size', 'ALL')
            cart_type = search_by.get('cart_type', 'ALL')
            service_status = search_by.get('status', 'ALL')
            service_type = search_by.get('service', 'ALL')
            processed = search_by.get('processed', 'True')

            sort_by = self.request.QUERY_PARAMS.get('sort_by', None)

            try:
                if sort_by:
                    query = Ticket.on_site.order_by(sort_by)
                else:
                    query = Ticket.on_site.filter()

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
                return query
            except:
                raise Http404
        else:
            raise Http404

    #over ride list method to provide csv download
    def list(self, request, *args, **kwargs):
        if self.request.accepted_renderer.format == "csv":
            file_name = self.request.QUERY_PARAMS.get('file_name', 'cart_logic_%s' % str(datetime.now().isoformat()))
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s.csv' % file_name
            t = loader.get_template('ticket.csv')
            c = Context({'data': self.get_queryset()}, )
            response.write(t.render(c))
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
                location = CollectionAddress(site=get_current_site(self.request), house_number=house_number.strip(), street_name=street_name.strip().upper(),
                    unit=unit, zipcode=zipcode, property_type=property_type, city=city, state=state, latitude=latitude, longitude=longitude,
                    geocode_status=geocode_status,customer=customer)
                location.save()
                return RestResponse({'details':{'message': "Saved new address: %s  for customer: %s" %
                (location, customer._get_full_name()), 'message_type': 'Success'}},
                    status=django_rest_status.HTTP_200_OK)
            else:
                location = self.get_object(location_id)
                if operation == 'remove':
                #Make sure the customer is current assigned to the address #TODO test else
                    if location.customer == customer:
                        location.customer = None
                        location.save()
                        return RestResponse({'details':{'message': "Removed address: %s  for customer: %s" %(location, customer._get_full_name()), 'message_type': 'Success'}},
                            status=django_rest_status.HTTP_200_OK)
                    else:
                        return RestResponse({'details':{'message': "Address: %s  does not have customer: %s" %(location, customer._get_full_name()), 'message_type': 'Failed'}},
                            status=django_rest_status.HTTP_200_OK)
                elif operation == 'change':
                    current_customer = location.customer
                    location.customer = customer
                    location.save()
                    return RestResponse({'details':{'message': "Changed address: %s  from: %s to: %s" %(location, current_customer._get_full_name(),customer._get_full_name() ), 'message_type': 'Success'}},
                        status=django_rest_status.HTTP_200_OK)
                elif operation == None:
                    return RestResponse({'details':{'message': "No operation value given", 'message_type': 'Failed'}},
                        status=django_rest_status.HTTP_200_OK)
        else:
            return RestResponse({'details':{'message': "No customer information received", 'message_type': 'Failed'}},
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

    def post(self, request, serial_number, format=None):
        try:
            cart = self.get_object(serial_number)
            json_data = simplejson.loads(request.raw_post_data)


            #grabbing values to be updated or None
            cart_type_id = json_data.get('cart_type', None)
            current_status_id = json_data.get('current_status', None)
            location_id = json_data.get('location_id', None)
            latitude = json_data.get('latitude', None)
            longitude = json_data.get('longitude', None)

            #check for cart type and save to cart, if None then no value given skip it
            if cart_type_id:
                cart.cart_type = CartType.objects.get(pk=cart_type_id)

            #check for current status
            if current_status_id:
                cart.current_status = CartStatus.on_site.get(pk=current_status_id)

            #check for location and update latitude + longitude to collection address lat and long
            if location_id:
                cart.location = CollectionAddress.on_site.get(pk=location_id)
                cart.last_latitude = cart.location.latitude
                cart.last_longitude = cart.location.longitude

            #check for latitude and longitude (map moves)
            if latitude and longitude:
                cart.last_latitude = latitude
                cart.last_longitude = longitude

            cart.save()
            #RestResponse({'details':{'message':'Success! New %s Ticket(s) created for %s' % (requested_service_type, location), 'message_type': 'Success'}}, status=django_rest_status.HTTP_201_CREATED)
            return RestResponse({"details": {'message': "Update complete for %s " % serial_number, 'message_type': 'Success',  "time": datetime.now()}}, status=django_rest_status.HTTP_200_OK)
        except Exception as e:
            return RestResponse(
                {"details": { 'message': "Darn, cart did not update, somethings wrong with the value for: %s" % (e), 'message_type':'Failed', "time": datetime.now()}}, status=django_rest_status.HTTP_200_OK)


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
                return RestResponse({
                "detail": {"Sorry! can not find ticket with id: '%s'" % (ticket_id)},
                "time": datetime.now()})
        except ValueError:
            #except ValueError if ticket_id is not an number
            return RestResponse({
            "detail": {"Sorry! ticket ids are numbers, not ...'%s!'" % (ticket_id)},
            "time": datetime.now()})

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
                       location = CollectionAddress.on_site.get(house_number=house_number, street_name=street_name, unit=unit)
                    else:
                        #ok no unit so just get the address using the house number and street name
                        print house_number, street_name

                        location = CollectionAddress.on_site.get(house_number=house_number, street_name=street_name)

                else:
                    return RestResponse({
                        "detail": {"No address information given"},
                        "time": datetime.now()})


                #Get the current service type and a cart service status object of requested
                requested_service_type = json_data.get('service_type', None)
                requested_ticket_status = TicketStatus.on_site.get(service_status='Requested')
                expected_cart_serial_number = json_data.get('cart_serial_number', None)
                size = json_data.get('cart_size', None)
                cart_type_name = json_data.get('cart_type', None)

                #If we have an expected cart serial number it is a remove, exchange, repair or audit
                #TODO put repair or audits in here
                if expected_cart_serial_number:
                    expected_cart = Cart.on_site.get(serial_number=expected_cart_serial_number)
                    if requested_service_type == 'Exchange' or 'Remove':
                        if requested_service_type == 'Exchange':
                            service_type_remove = CartServiceType.on_site.get(code='EX-REM')
                        else:
                            print requested_service_type
                            service_type_remove = CartServiceType.on_site.get(code='REM')

                        remove_ticket = Ticket(created_by=request.user, location=location,
                                                          status=requested_ticket_status,
                                                          expected_cart=expected_cart,
                                                          service_type=service_type_remove,
                                                          cart_type=expected_cart.cart_type
                                                          )
                        remove_ticket.save()

                #Create service ticket or tickets below, some code repeated but feels more readable

                if requested_service_type == 'Delivery':
                    #Delivery? You should get and add the cart type from cart type name and size
                    #Create a new delivery ticket service type of code DEL.
                    service_type = CartServiceType.on_site.get(code='DEL')
                    cart_type = CartType.on_site.get(name=cart_type_name, size=size)
                    delivery_ticket = Ticket(created_by=request.user, location=location,service_type=service_type,
                                                        status= requested_ticket_status,
                                                        cart_type=cart_type,
                                                        )
                    delivery_ticket.save()



                elif requested_service_type == 'Exchange':
                    #Exchange? You should get and add the cart type from name and size
                    #Create a new delivery ticket with service type EX-DEL and remove ticket with service type EX-REM,
                    service_type = CartServiceType.on_site.get(code='EX-DEL')
                    cart_type = CartType.on_site.get(name=cart_type_name, size=size)
                    exchange_del_ticket = Ticket(created_by=request.user, location=location, service_type=service_type,
                                                            status= requested_ticket_status,
                                                            cart_type=cart_type
                                                            )
                    exchange_del_ticket.save()

                return RestResponse({'details':{'message':'Success! New %s Ticket(s) created for %s' % (requested_service_type, location), 'message_type': 'Success'}}, status=django_rest_status.HTTP_201_CREATED)

            except Exception as e:
                return RestResponse({'details':{'message': "Sorry! ticket could not be created, code: %s" % e, 'message_type': 'Failed'}},
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
                        return RestResponse({'details':{'message':
                            'Could not find  a cart with serial number: %s' % serial_number, 'message_type': 'Fail'}},
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
                return RestResponse({'details':{'message': 'Ticket: %s has been updated' % ticket_id,

                                    'message_type': 'Success'}},
                        status=django_rest_status.HTTP_200_OK)

            except ValueError as e:
                #TODO beef up the error response ...to generic

                return RestResponse({'details':{'message': "Sorry! ticket could not be updated: %s" % e, 'message_type': 'Failed'}},
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
            serializer =  TicketCommentSerializer(comments)
            return RestResponse(serializer.data)
        else:
            return RestResponse({'details':{'message': 'Nothing to say...', 'count': 0, 'message_type': 'Success'}},
                status=django_rest_status.HTTP_200_OK)

    def post(self, request, ticket_id, format=None):

        json_data = simplejson.loads(request.body)
        comment = json_data.get('text', None)
        ticket = Ticket.on_site.get(pk=ticket_id)

        if comment:
            new_comment = TicketComments(site=get_current_site(self.request), text=comment, ticket=ticket, created_by=self.request.user)
            new_comment.save()

            return RestResponse({'details':{'message': "Comment Saved", 'message_type': 'Success', 'comment_id': new_comment.id}},
                status=django_rest_status.HTTP_200_OK)
        else:
            return RestResponse({'details':{'message': "No text given", 'message_type': 'Failed'}},
                status=django_rest_status.HTTP_200_OK)

    def delete(self, request, ticket_id, format=None):
        json_data = simplejson.loads(request.body)
        comment_id = json_data.get('comment_id', None)
        try:
            comment = TicketComments.on_site.get(pk=comment_id)
            if comment.created_by == request.user:
                comment.delete()
                return RestResponse({'details':{'message': "Comment has been deleted", 'message_type': 'Success'}},
                status=django_rest_status.HTTP_200_OK)
        except TicketComments.DoesNotExist:
            return RestResponse({'details':{'message': "Comment Does not exist", 'message_type': 'Failed'}},
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

        if (first_name and last_name and phone_number):
            customer.first_name = first_name.upper()
            customer.last_name = last_name.upper()
            customer.email = email.upper()
            customer.phone_number = phone_number
            customer.save()

            return RestResponse({"details":{"message": "Changes saved for customer: %s" % (customer._get_full_name()), "customer_id":customer.id,  "message_type": "Success"}},
                                status=django_rest_status.HTTP_200_OK)

        else:
            return RestResponse({'details':{'message': "Missing one or more values", 'message_type': 'Failed'}},
                                    status=django_rest_status.HTTP_200_OK)



##TODO thinking about a change location update only
#class UpdateCartLocationAPI(RetrieveModelMixin,UpdateModelMixin, SingleObjectAPIView ):
#    model = Cart
#    serializer_class = CartLocationUpdateSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)


class CartStatusAPI(ListAPIView):
    model = CartStatus
    serializer_class = CartStatusSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        return  CartStatus.on_site.all()

class TicketStatusAPI(ListAPIView):
    model = TicketStatus
    serializer_class = TicketStatusSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        return  TicketStatus.on_site.all()

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


########################################################################################################################
#End of API Views
########################################################################################################################

class DataErrorsView(ListView):
    template_name = 'uploaderrors.html'
    context_object_name = "data_errors"
    queryset = DataErrors.on_site.filter(fix_date__isnull=True)
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(DataErrorsView, self).get_context_data(**kwargs)
        return context


#class UploadFormView(FormView):
#    """
#     A base view for rendering upload forms.
#
#     Subclasses FormView from django.
#     Expects process boolean and csv file type
#
#    """
#    template_name = 'upload_form.html'
#    form_class = None
#    MODEL = None
#    FILE = None
#    KIND = None
#    LINK = None
#
#
#    def form_valid(self, form, **kwargs):
#        if self.request.POST.get('process'):
#            process = True
#        else:
#            process = False
#        context = self.get_context_data(**kwargs)
#        upload_file = self.MODEL
#        file = self.request.FILES[self.FILE]
#
#        if file.content_type == "application/vnd.ms-excel" or "text/csv":
#            upload_file.file_path =  file
#            upload_file.size = file.size
#            upload_file.records_processed = process
#            upload_file.file_kind = self.KIND
#            upload_file.site = Site.objects.get(id=get_current_site(self.request).id)
#            upload_file.uploaded_by = self.request.user
#            upload_file.save()
#            total_count, good_count, error_count = upload_file.process(process)
##            context['total_count'] = total_count
##            context['good_count'] = good_count
##            context['error_count'] = error_count
##            context['form'] = self.form_class
##            context['link'] = self.LINK
##            context['completed'] = True
##            return self.render_to_response(context)
#
#            return self.render_to_response({'details':{'message': "Saved %s" % self.FILE, "total_count": total_count, "good_count": good_count, 'message_type': 'Success'}},
#                status=django_rest_status.HTTP_200_OK)

class UploadFormView(TemplateView):
    """
     A base view for uploading files

     Subclasses API View.
     Expects process boolean and csv file type

    """
    template_name = 'upload_form.html'

    MODEL = None
    FILE = None
    KIND = None
    LINK = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['link'] = self.LINK
        return self.render_to_response(context)


    def post(self, request, **kwargs):
        #TODO implement processing option
        #TODO for now it is just True
        process = request.POST.get('process', True)
        context = self.get_context_data(**kwargs)
       #TODO Remove upload_file = self.MODEL()
        upload_file = self.MODEL()
        file = self.request.FILES['upload_file']
        #looks for csv type file
        if file.content_type == "application/vnd.ms-excel" or "text/csv":
            upload_file.file_path =  file
            upload_file.size = file.size
            upload_file.records_processed = False
            upload_file.file_kind = self.KIND
            upload_file.status = 'UPLOADED'
            upload_file.site = Site.objects.get(id=get_current_site(self.request).id)
            upload_file.uploaded_by = self.request.user
            upload_file.save()
            #Here the records are processed
            #process_upload_records(self.MODEL, upload_file.site, upload_file.id)
            enqueue(func=process_upload_records, args=(self.MODEL, upload_file.site, upload_file.id))
            #total_count, good_count, error_count = (1,2,3)
            total_count, good_count, error_count = (1,2,3) #upload_file.process(process)
            return HttpResponse(simplejson.dumps({'details':{'message': "Saved %s" % self.FILE,
                                                 "total_count": total_count, "good_count": good_count,
                                                  "error_count": error_count, 'message_type': 'Success'}}),
                                                  content_type="application/json")
class CartUploadView(UploadFormView):
    #form_class = CartsUploadFileForm
    MODEL = CartsUploadFile
    FILE = 'cart_file'
    KIND = 'Cart'
    LINK = 'Cart File Upload'


class CustomerUploadView(UploadFormView):
    #form_class = CustomerUploadFileForm
    MODEL = CustomersUploadFile()
    FILE = 'customer_file' #is an attribute on CustomerUploadFileForm
    KIND = 'Customer'
    LINK = 'Customer File Upload'


class TicketsCompletedUploadView(UploadFormView):
    form_class = TicketsCompletedUploadFileForm
    MODEL = TicketsCompleteUploadFile()
    FILE = 'ticket_file'
    KIND = 'Ticket'
    LINK = 'Ticket Upload'
