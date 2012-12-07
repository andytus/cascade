import csv
from django.shortcuts import render_to_response, render, get_object_or_404
from models import *
from django.views.generic import FormView, TemplateView, ListView
from django.http import Http404
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import MultipleObjectAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin

from serializer import CartLocationSearchSerializer, CartDetailsSerializer


class LocationSearchAPI(ListAPIView):
    model = Cart
    serializer_class = CartLocationSearchSerializer
    house_number = None
    address = None
    serial_number = None
    size = None
    cart_type = None
    search_type = None

    def get(self, request, *args, **kwargs):
        """
        Gets all the expected query parameters and assigns them.
        """
        self.house_number = request.QUERY_PARAMS.get('address').split(' ')[0]  or None
        self.street_name = request.QUERY_PARAMS.get('address').split(' ')[1] or None
        self.serial_number = request.QUERY_PARAMS.get('serial_number') or None
        self.size = request.QUERY_PARAMS.get('size') or None
        self.type = request.QUERY_PARAMS.get('type') or None
        self.search_type = request.QUERY_PARAMS.get('search') or None
        return self.list(self, request, *args, **kwargs)

    def get_queryset(self):
        """
        Performs search query for Carts
        """
        query = Cart.objects.all()
        if self.house_number and self.street_name:
            return query.filter()



        return query




#    def get_queryset(self):
#        """
#        Performs the search query.
#        """
#        query = CollectionAddress.objects.all()
#        if self.search_type == 'location':
#            if self.house_number and self.street_name:
#                return query.filter(house_number=self.house_number, street_name=self.street_name)
#        elif self.search_type == 'cart':
#            if self.serial_number:
#                return query.filter(location__serial_number= self.serial_number)
#
#            elif self.search_type == 'customer':
#                pass
#        else:
#            raise Http404



class CartDetailAPI(RetrieveAPIView):
    model=Cart
    serializer_class = CartDetailsSerializer

class  CustomerDetailAPI(RetrieveAPIView):
    pass


#class CartSearchAPI(ListAPIView):
#    model=Cart
#    serializer_class = CartSearchSerializer
#    serial = None
#
#    def get(self, request, *args, **kwargs):
#        self.serial = request.QUERY_PARAMS.get('serial_number')
#
#        return self.list(self, request, *args, **kwargs)
#
#    def get_queryset(self):
#        if self.serial:
#            query = Cart.objects.filter(serial_number=self.serial)
#            if query:
#                return query
#            else:
#                raise Http404



#class CartSearchAPI(ListModelMixin, MultipleObjectAPIView):
#    model=Cart
#    serializer_class = CartSerializer
#    #queryset = Cart.objects.all()
#
#    def get_queryset(self):
#        print(self.request)
#        if self.:
#            query = Cart.objects.filter(serial=self.kwargs['serial'])
#        return query
#
#
#    def get_object(self):
#        try:
#            return Cart.objects.all()
#        except Cart.DoesNotExist:
#            raise Http404
#
#    def get(self, request, *args, **kwargs):
#
#        #print request.QUERY_PARAMS.get('serial')
#        #TODO Try Except ...iterate QUERY PARAMS...raise 404 (maybe just some ifs)
#        return self.list(self, request, *args, **kwargs)



class CartUpdateAPI(TemplateView):
    pass



class DataErrorsView(ListView):
    template_name = 'uploaderrors.html'
    context_object_name = "data_errors"
    queryset = DataErrors.objects.filter(fix_date__isnull=True)
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

        if file.content_type == "application/vnd.ms-excel":
            upload_file.file_path = file
            upload_file.size = file.size
            upload_file.file_kind = self.KIND
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

        query = CartServiceTicket.objects.values('cart__rfid','location__street_name', 'location__house_number', 'location__unit', 'service_type', 'id' )

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
                return "test"
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
















