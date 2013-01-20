import csv
from django.shortcuts import  render
from django.contrib.sites.models import get_current_site
from cascade.apps.cartmanager.models import *
from django.views.generic import FormView, TemplateView, ListView
from django.http import Http404
from django.http import HttpResponse
from rest_framework.generics import  ListAPIView, RetrieveUpdateDestroyAPIView, SingleObjectAPIView
from rest_framework.mixins import  RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer

from cascade.apps.cartmanager.serializer import CartSearchSerializer, CartProfileSerializer, CustomerProfileSerializer, AddressProfileSerializer, \
    CartLocationUpdateSerializer, CurrentStatusSerializer

from cascade.libs.mixins import LoginSiteRequiredMixin


class CartSearch(LoginSiteRequiredMixin,TemplateView):
    template_name = 'cart_search.html'
    search_query = None

    def get_context_data(self, **kwargs):
        context = super(CartSearch, self).get_context_data(**kwargs)
        #TODO Create a default search query ... selecting the last 50 modified and remove the raise
        search_parameters = self.request.GET.get('search_query', None)
        if search_parameters:
            context['search_parameters'] = self.request.GET['search_query']
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




######################################################################################################################
#API VIEWS: Used to render, create and update content to applications                                                #
######################################################################################################################

class CartSearchAPI(LoginSiteRequiredMixin, ListAPIView):
    model = Cart
    serializer_class = CartSearchSerializer
    paginate_by = 15
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        """
        Performs search query for Carts
        """
        query = Cart.on_site.filter()
        search_type = self.request.QUERY_PARAMS.get('type', None)
        value = self.request.QUERY_PARAMS.get('value', None)

        if search_type and value:
            if search_type == 'address':
                query = query.filter(location__street_name=value.split(' ')[1], location__house_number = value.split(' ')[0])
            elif search_type == 'serial_number':
                query = query.filter(serial_number__contains=str(value))
            elif search_type == 'type':
                query = query.filter(cart_type=value)
            elif  search_type == 'size':
                query = query.filter(size=value)
            else:
                raise Http404
        else:
            raise Http404
        return query


class LocationProfileAPI(RetrieveUpdateDestroyAPIView):
    model = CollectionAddress
    serializer = AddressProfileSerializer

class CartProfileAPI(RetrieveUpdateDestroyAPIView):
    model=Cart
    serializer_class = CartProfileSerializer
    renderer_classes = (JSONPRenderer, JSONRenderer, BrowsableAPIRenderer)

    def get_object(self, serial_number):
        try:
            return Cart.objects.get(serial_number=serial_number)
        except Cart.DoesNotExist:
            return Http404

    def get(self, request, serial_number, format=None):
        cart = self.get_object(serial_number)
        serializer = CartProfileSerializer(cart)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pass

class CustomerProfileAPI(RetrieveUpdateDestroyAPIView):
    model=CollectionCustomer
    serializer_class = CustomerProfileSerializer

#TODO thinking about a change location update only
class UpdateCartLocationAPI(RetrieveModelMixin,UpdateModelMixin, SingleObjectAPIView ):
    model = Cart
    serializer_class = CartLocationUpdateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CartStatusAPI(ListAPIView):
    model=CartStatus
    serializer_class = CurrentStatusSerializer


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
        context = self.get_context_data(**kwargs)
        upload_file = self.MODEL
        file = self.request.FILES[self.FILE]

        if file.content_type == "application/vnd.ms-excel" or "text/csv":
            upload_file.file_path = file
            upload_file.size = file.size
            upload_file.file_kind = self.KIND
            upload_file.site = Site.objects.get(id=get_current_site(self.request).id)
            upload_file.save()
            total_count, good_count, error_count = upload_file.process()
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

class CSVResponseMixin(object):
    """
    This mixin works renders a csv file using render_to_response method.
    It currently only works with a ValuesQuerySet as part of the context.
    You must also create a csv_header context for column headings in the
    generic views get_context_object.

    """
    #inspired by http://palewi.re/posts/2009/03/03/django-recipe-dump-your-queryset-out-as-a-csv-file/

    def render_to_response(self, context,**httpresponse_kwargs ):
        """Constructs HttpResponse and send to the convert_to_csv for write to csv.
           Return CSV containing 'context' as payload"""

        header = []
        if  context['csv_header']:
            header = context['csv_header']
        self.response =HttpResponse(mimetype="text/csv",  **httpresponse_kwargs)
        self.response['Content-Disposition']= 'attachment; filename=import.csv'
        self.response['content'] = self.convert_to_csv(context[self.context_object_name], header)

        return self.response


    def convert_to_csv(self, context, header):
        writer = csv.writer(self.response)
        #fields come from ValuesQuerySet keys (acts like a dictionary)
        context_fields = context[0].keys()
        context_fields.sort()
        writer.writerow(header)

        for obj in context:
            row = []
            for field in context_fields:
                #iterate through values in each context object
                #check for correct encoding (python csv doesn't like unicode)
                val = obj[field]
                if type == unicode:
                    val = val.encode('utf-8')
                row.append(val)
            writer.writerow(row)
        return writer

class TicketsDownloadView(CSVResponseMixin, ListView):
    template_name = 'ticketdownload.html'
    context_object_name = 'tickets'

    def get_queryset(self):

        query = CartServiceTicket.on_site.values('cart__rfid','location__street_name', 'location__house_number', 'location__unit', 'service_type', 'id' )

        if self.kwargs['status'] != 'all':
            query = query.filter(status=self.kwargs['status'])
        if self.kwargs['cart_type'] != 'all':
            query = query.filter(cart_type=self.kwargs['cart_type'])
        if self.kwargs['service_type'] != 'all':
            query = query.filter(service_type__contains=self.kwargs['service_type'])
        return query

    def get_context_data(self, **kwargs):
        context = super(TicketsDownloadView, self).get_context_data(**kwargs)
        return context

    def render_to_response(self, context,**httpresponse_kwargs ):

        if not context[self.context_object_name]:
            context["message"] = "No Values"
            return render(self.request, self.template_name, context)
        else:
            if self.request.GET.get('format', 'html') == 'csv':
                context['csv_header'] = ['RFID', 'SystemID', 'HouseNumber', 'StreetName', 'UnitNumber', 'ServiceType']
                return CSVResponseMixin.render_to_response(self, context)
            elif self.request.GET.get('format', 'html') == 'json':
                #TODO get json
                context["message"] = "json"
                #TODO
                #return render(self.request, self.template_name, context)
            else:
                #TODO html page
                context["message"] = "just html here"
                return render(self.request, self.template_name, context)

class TicketsCompletedUploadView(UploadFormView):
    form_class = TicketsCompletedUploadFileForm
    MODEL = TicketsCompleteUploadFile()
    FILE  = 'ticket_file'
    KIND =  'Ticket'
    LINK =  'Ticket Upload'
















