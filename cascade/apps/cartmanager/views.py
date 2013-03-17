import csv
from django.shortcuts import  render
from django.utils import simplejson
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from cascade.apps.cartmanager.models import *
from django.template import loader, Context
from django.views.generic import FormView, TemplateView, ListView
from django.http import Http404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, MultipleObjectAPIView
from rest_framework.mixins import  RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from cascade.libs.renderers import CSVRenderer
from django.db.models import Q

from cascade.apps.cartmanager.serializer import LocationInfoSerializer, CartSearchSerializer, CartProfileSerializer, CustomerProfileSerializer, AddressCartProfileSerializer,\
    CartStatusSerializer, CartTypeSerializer, CartServiceTicketSerializer
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
                    #TODO Change to address!
                    #Just sending back the location id, the client can look up the address info using the API
                    #only needed for deliveries can get location id from cart for other request
                    print location_id
                    context['location_id'] = location_id

                cart_id = self.request.GET.get('cart_id', None)
                #TODO change to serial number
                if cart_id:
                    #send over the cart id to use in the Ticket API and the cart serial for user verification.
                    #Note: should use cart serial but currently can not be trusted as unique for each account
                    cart = Cart.on_site.get(pk=cart_id)
                    context['cart_id'] = cart_id
                    context['cart_address_house_number'] = cart.location.house_number
                    context['cart_address_street_name'] = cart.location.street_name
                    context['cart_address_unit'] = cart.location.unit
                    context['serial_number'] = cart.serial_number
        else:
            raise Http404
        return context


class TicketOpen(LoginSiteRequiredMixin, TemplateView):
    template_name = "ticket_open.html"


######################################################################################################################
#API VIEWS: Used to render, create and update content to applications                                                #
######################################################################################################################

class CartSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    model = Cart
    serializer_class = CartSearchSerializer
    paginate_by = 50
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
            return Response({"detail":"No Search values received...try again. "}, status=status.HTTP_404_NOT_FOUND)











class TicketSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    #TODO make this api except json list of values to filter for each parameter (i.e. select multiple)
    model = CartServiceTicket
    serializer_class = CartServiceTicketSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer, CSVRenderer, JSONPRenderer, BrowsableAPIRenderer,)
    paginate_by = 10


    def get_queryset(self):
        cart_serial = self.request.QUERY_PARAMS.get('serial_number', None)
        cart_size = self.request.QUERY_PARAMS.get('cart_size', 'ALL')
        cart_type = self.request.QUERY_PARAMS.get('cart_type', 'ALL')
        service_status = self.request.QUERY_PARAMS.get('status', 'ALL')
        service_type = self.request.QUERY_PARAMS.get('service', 'ALL')
        processed = self.request.QUERY_PARAMS.get('processed', 'True')
        sort_by = self.request.QUERY_PARAMS.get('sort_by', None)

        try:
            if sort_by:
                query = CartServiceTicket.on_site.order_by(sort_by)
            else:
                query = CartServiceTicket.on_site.filter()

            if  cart_serial:
                query = query.filter(
                    Q(expected_cart__serial_number=cart_serial) | Q(serviced_cart__serial_number=cart_serial))
            else:
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
            return Http404

    #over ride list method to provide csv download
    def list(self, request, *args, **kwargs):
        if self.request.accepted_renderer.format == "csv":
            file_name = self.request.QUERY_PARAMS.get('file_name', 'import')
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s.csv' % file_name
            t = loader.get_template('ticket.csv')
            c = Context({'data': self.get_queryset()}, )
            response.write(t.render(c))
            return response

        return super(TicketSearchAPI, self).list(request, *args, **kwargs)


class LocationProfileAPI(LoginSiteRequiredMixin, APIView):
    model = CollectionAddress
    serializer = AddressCartProfileSerializer


class LocationSearchAPI(LoginSiteRequiredMixin, APIView):
    def get_queryset(self, address, address_id):
        try:
            if address:
                house_number = address.split(' ')[0].strip().upper()
                street_name = address.split(house_number)[1].strip().upper()
                query = CollectionAddress.on_site.filter(house_number=house_number, street_name__contains=street_name)
                return query
            elif address_id:
                query = CollectionAddress.on_site.get(pk=address_id)
                return query
            else:
                raise Http404
        except:
            raise Http404


    def get(self, request, format=None):
        address = self.request.QUERY_PARAMS.get('address', None)
        address_id = self.request.QUERY_PARAMS.get('address_id', None)
        addresses = self.get_queryset(address, address_id)
        serializer = LocationInfoSerializer(addresses)
        return Response(serializer.data)


class CartProfileAPI(LoginSiteRequiredMixin, APIView):
    model = Cart
    serializer_class = CartProfileSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, serial_number):
        try:
            return Cart.on_site.get(serial_number=serial_number)
        except Cart.DoesNotExist:
            return Http404

    def get(self, request, serial_number, format=None):
        #TODO need to redirect if cart does not exist (i.e. http404-location does not exist).. look for fix in serializer
        cart = self.get_object(serial_number)
        serializer = CartProfileSerializer(cart)

        if request.accepted_renderer.format == 'csv':
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=profile.csv'
            t = loader.get_template('profile.csv')
            c = Context({'data': cart}, )
            response.write(t.render(c))
            return response
        return Response(serializer.data)

    def post(self, request, serial_number, format=None):
        try:
            cart = self.get_object(serial_number)
            json_data = simplejson.loads(request.raw_post_data)
            cart_type = CartType.on_site.get(pk=json_data['cart_type'])
            current_status = CartStatus.on_site.get(pk=json_data['current_status'])
            cart.cart_type = cart_type
            cart.current_status = current_status
            cart.last_updated = datetime.now()
            cart.save()

            return Response({"message": "Update Complete...all set!", "time": datetime.now()})
        except Exception as e:
            #TODO Test this error
            return Response(
                {"Error": "Error: Sorry, did not update, somethings wrong:%s" % (e), "time": datetime.now()})


class TicketAPI(APIView):
    model = CartServiceTicket
    serializer_class = CartServiceTicketSerializer
    renderer_classes = (CSVRenderer, JSONPRenderer, JSONRenderer, BrowsableAPIRenderer,)

    def get_object(self, ticket_id):
        try:
            ticket = CartServiceTicket.on_site.get(id=ticket_id)
            return ticket

        except ObjectDoesNotExist:
            return None

    def get(self, request, ticket_id, format=None):
        try:
            ticket = self.get_object(ticket_id)
            if ticket:
                serializer = CartServiceTicketSerializer(ticket)
                return Response(serializer.data)
            else:
                return Response({
                "Message": {"Type": "Error", "Description": "Sorry! can not find ticket with id: '%s'" % (ticket_id)},
                "time": datetime.now()})
        except ValueError:
            #except ValueError if ticket_id is not an number
            return Response({
            "Message": {"Type": "Error", "Description": "Sorry! ticket ids are numbers, not ...'%s!'" % (ticket_id)},
            "time": datetime.now()})

    def post(self, request, ticket_id, format=None):
        json_data = simplejson.loads(request.raw_post_data)
        print json_data
        if ticket_id == 'New':
            try:
                #TODO don't create early may need two: ticket = CartServiceTicket.on_site.create()
                #excepts both location id and address for the Collection Address
                if json_data['location_id']:
                    location = CollectionAddress.on_site.get(pk=json_data['location_id'])
                elif json_data['address']:
                    house_number = json_data['address'].split(' ')[0].strip().upper()
                    street_name = json_data['address'].split(house_number)[1].strip().upper()
                    location = CollectionAddress.on_site.get(house_number=house_number, street_name=street_name)


                location = CollectionAddress()
                #Get the service type
                requested_service_type = json_data['service_type']

                status = CartServiceStatus.on_site.get(service_status='Requested')

                #check the codes and create ticket with appropriate information
                if requested_service_type == 'Delivery' or requested_service_type == 'Exchange':
                    new_service_type = CartServiceType.on_site.get(service=json_data['service_type'])
                    cart_type = CartType.on_site.get(name=json_data['cart_type'], size=json_data['size'])
                    del_ticket = CartServiceTicket(location=location, service_type=new_service_type,
                        cart_type=cart_type,
                        status=status)
                    del_ticket.save()

                else:
                    # if its not a Delivery it will be an Exchange or Removal and we need to get the cart before creating
                    # either one ticket for a Removals (REM) or two for Exchanges (EX-DEL, EX-REM)
                    if json_data['serial_number']:
                        expected_cart = Cart.on_site.get(serial_number=json_data['serial_number'])
                    elif json_data['rfid']:
                        expected_cart = Cart.on_site.get(serial_number=json_data['rfid'])
                    else:
                        #have to use the cart id as the serial number is unreliable (i.e. could get duplicate data from production)
                        expected_cart = Cart.on_site.get(pk=json_data['cart_id'])

                    if requested_service_type == 'Exchange':
                        #Assigning the expected cart, using expected cart type for ticket cart type (important for ticket export fields: rifd, size),
                        #using EX-REM (exchange removal) for service type. Also use the expected cart location for the location.
                        rem_ticket = CartServiceTicket(expected_cart=expected_cart, location=expected_cart.location,
                            service_type=CartServiceTicket(code='EX-REM'),
                            cart_type=expected_cart.cart_type, status=status)
                        rem_ticket.save()
                        #get cart type for the new exchange delivery ticket (repeated code above, refactor in future)
                        cart_type = CartType.on_site.get(name=json_data['cart_type'], size=json_data['size'])
                        #Using EX-DEL (exchange delivery for the service type
                        del_ticket = CartServiceTicket(location=expected_cart.location,
                            service_type=CartServiceTicket(code='EX-DEL'), cart_type=cart_type,
                            status=status)
                        del_ticket.save()

                    if requested_service_type == "Removal":
                        #Assing the expected cart, using expected cart type for ticket cart type (import for ticket export fields: rfid, size),
                        #using REM (removal) for service type. Also use the expected cart location for the location.
                        rem_ticket = CartServiceTicket(expected_cart=expected_cart, location=expected_cart.location,
                            service_type=CartServiceTicket(code='REM'),
                            cart_type=expected_cart.cart_type, status=status)
                        rem_ticket.save()
            except Exception as e:
                return Response({"Message": {"Type": "Error", "Description": "Sorry! ticket could not be created"},
                                "time": datetime.now()})

        else:
            #Expecting this to be a status change if it is not New
            #Change status of the ticket id
            try:
                ticket = self.get_object(ticket_id)
                update_status = json_data['status']
                status = CartServiceStatus.on_site.get(service_status=update_status)
                ticket.status = update_status
                ticket.save()
            except ValueError as e:
                 return Response({
                "Message": {"Type": "Error", "Description": "Sorry! ticket ids are numbers not ...'%s'" % (ticket_id)},
                "time": datetime.now()})


class CustomerProfileAPI(RetrieveUpdateDestroyAPIView):
    model = CollectionCustomer
    serializer_class = CustomerProfileSerializer

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
    queryset = CartStatus.on_site.filter()


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


class UploadFormView(FormView):
    template_name = 'upload_form.html'
    form_class = None
    MODEL = None
    FILE = None
    KIND = None
    LINK = None


    def form_valid(self, form, **kwargs):
        if self.request.POST.get('process'):
            process = True
        else:
            process = False
        context = self.get_context_data(**kwargs)
        upload_file = self.MODEL
        file = self.request.FILES[self.FILE]

        if file.content_type == "application/vnd.ms-excel" or "text/csv":
            upload_file.file_path = file
            upload_file.size = file.size
            upload_file.process_records = process
            upload_file.file_kind = self.KIND
            upload_file.site = Site.objects.get(id=get_current_site(self.request).id)
            upload_file.save()
            total_count, good_count, error_count = upload_file.process(process)
            context['total_count'] = total_count
            context['good_count'] = good_count
            context['error_count'] = error_count
            context['form'] = self.form_class
            context['link'] = self.LINK
            context['completed'] = True
            return self.render_to_response(context)


class CartUploadView(UploadFormView):
    form_class = CartsUploadFileForm
    MODEL = CartsUploadFile()
    FILE = 'cart_file'
    KIND = 'Cart'
    LINK = 'Cart File Upload'


class CustomerUploadView(UploadFormView):
    form_class = CustomerUploadFileForm
    MODEL = CustomersUploadFile()
    FILE = 'customer_file' #is an attribute on CustomerUploadFileForm
    KIND = 'Customer'
    LINK = 'Customer File Upload'


#class CSVResponseMixin(object):
#    """
#    This mixin works renders a csv file using render_to_response method.
#    It currently only works with a ValuesQuerySet as part of the context.
#    You must also create a csv_header context for column headings in the
#    generic views get_context_object.
#
#    """
#    #inspired by http://palewi.re/posts/2009/03/03/django-recipe-dump-your-queryset-out-as-a-csv-file/
#
#    def render_to_response(self, context,**httpresponse_kwargs ):
#        """Constructs HttpResponse and send to the convert_to_csv for write to csv.
#           Return CSV containing 'context' as payload"""
#
#        header = []
#        if  context['csv_header']:
#            header = context['csv_header']
#        self.response =HttpResponse(mimetype="text/csv",  **httpresponse_kwargs)
#        self.response['Content-Disposition']= 'attachment; filename=import.csv'
#        self.response['content'] = self.convert_to_csv(context[self.context_object_name], header)
#
#        return self.response
#
#
#    def convert_to_csv(self, context, header):
#        writer = csv.writer(self.response)
#        #fields come from ValuesQuerySet keys (acts like a dictionary)
#        context_fields = context[0].keys()
#        context_fields.sort()
#        writer.writerow(header)
#
#        for obj in context:
#            row = []
#            for field in context_fields:
#                #iterate through values in each context object
#                #check for correct encoding (python csv doesn't like unicode)
#                val = obj[field]
#                if type == unicode:
#                    val = val.encode('utf-8')
#                row.append(val)
#            writer.writerow(row)
#        return writer

#class TicketsDownloadView(CSVResponseMixin, ListView):
#    template_name = 'ticketdownload.html'
#    context_object_name = 'tickets'
#
#    def get_queryset(self):
#
#        query = CartServiceTicket.on_site.values('cart__rfid','location__street_name', 'location__house_number', 'location__unit', 'service_type', 'id' )
#
#
#        if self.kwargs['status'] != 'all':
#            query = query.filter(status=self.kwargs['status'])
#        if self.kwargs['cart_type'] != 'all':
#            query = query.filter(cart_type=self.kwargs['cart_type'])
#        if self.kwargs['service_type'] != 'all':
#            query = query.filter(service_type__contains=self.kwargs['service_type'])
#        return query
#
#    def get_context_data(self, **kwargs):
#        context = super(TicketsDownloadView, self).get_context_data(**kwargs)
#        return context
#
#    def render_to_response(self, context,**httpresponse_kwargs ):
#
#        if not context[self.context_object_name]:
#            context["message"] = "No Values"
#            return render(self.request, self.template_name, context)
#        else:
#            if self.request.GET.get('format', 'html') == 'csv':
#                context['csv_header'] = ['RFID', 'SystemID', 'HouseNumber', 'StreetName', 'UnitNumber', 'ServiceType']
#                return CSVResponseMixin.render_to_response(self, context)
#            elif self.request.GET.get('format', 'html') == 'json':
#                #TODO get json
#                context["message"] = "json"
#                #TODO
#                #return render(self.request, self.template_name, context)
#            else:
#                #TODO html page
#                context["message"] = "just html here"
#                return render(self.request, self.template_name, context)

class TicketsCompletedUploadView(UploadFormView):
    form_class = TicketsCompletedUploadFileForm
    MODEL = TicketsCompleteUploadFile()
    FILE = 'ticket_file'
    KIND = 'Ticket'
    LINK = 'Ticket Upload'
















