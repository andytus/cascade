import csv
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.shortcuts import render_to_response, render, get_object_or_404
from models import *
from django.views.generic import FormView,TemplateView, ListView
from django.http import HttpResponse


class DataErrorsView(ListView):
    #TODO Change to a queryset of objects to operate on (get only recent errors) i.e parameter of last 5 days
    #TODO ...then query based on date.
    template_name = '../cascade/templates/cartmanager/uploaderrors.html'
    context_object_name = "data_errors"
    queryset = DataErrors.objects.filter(fix_date__isnull=True)
    #for all DataErrors use model
    #model = DataErrors

    def get_context_data(self, **kwargs):
        context = super(DataErrorsView, self).get_context_data(**kwargs)
        return context

class UploadFormView(FormView):
    template_name = '../cascade/templates/cartmanager/upload_form.html'
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
    template_name = '../cascade/templates/cartmanager/ticketdownload.html'
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
                return render(self.request, self.template_name, context)
            else:
                #TODO html page
                context["message"] = "just html here"
                return render(self.request, self.template_name, context)


class TicketsCompletedUploadView(UploadFormView):
    form_class = TicketsCompletedUploadFileForm
    MODEL = TicketsCompleteUploadFile()
    FILE  = 'ticket_file'
    KIND = 'Ticket'
    LINK = 'Ticket Upload'
















