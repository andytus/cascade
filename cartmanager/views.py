from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.shortcuts import render_to_response, render
from models import Cart, CartsUploadFile, CartsUploadFileForm, DataErrors, CustomersUploadFile, CustomerUploadFileForm
from django.views.generic import FormView,TemplateView, ListView
from django.http import HttpResponse


class DataErrorsView(ListView):
    #TODO Change to a queryset of objects to operate on (get only recent errors)
    template_name ='uploaderrors.html'
    context_object_name = "data_errors"
    queryset = DataErrors.objects.filter(fix_date__isnull=True)
    #for all DataErrors use mode
    #model = DataErrors

    def get_context_data(self, **kwargs):
        context = super(DataErrorsView, self).get_context_data(**kwargs)
        return context

class UploadForm(FormView):
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
        print file
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

class CartUploadView(UploadForm):
    form_class = CartsUploadFileForm
    MODEL = CartsUploadFile()
    FILE = 'cart_file'
    KIND = 'Cart'
    LINK = 'Cart File Upload'

class CustomerUploadView(UploadForm):
    form_class = CustomerUploadFileForm
    MODEL = CustomersUploadFile()
    FILE = 'customer_file' #is an attribute on CustomerUploadFileForm
    KIND = 'Customer'
    LINK = 'Customer File Upload'



#class CartUploadView(FormView):
#    template_name = 'cart_upload.html'
#    form_class = CartsUploadFileForm
#
#    def form_valid(self, form, **kwargs):
#        context = self.get_context_data(**kwargs)
#        upload_file = CartsUploadFile()
#        cart_file = self.request.FILES['cart_file']
#        if cart_file.content_type == "application/vnd.ms-excel":
#            upload_file.file_path = cart_file
#            upload_file.size = cart_file.size
#            upload_file.file_kind = 'Carts'
#            upload_file.save()
#            total_count, good_count, error_count = upload_file.process()
#            context['total_count'] = total_count
#            context['good_count'] = good_count
#            context['error_count'] = error_count
#            context['form'] = self.form_class
#            context['completed'] = True
#            return self.render_to_response(context)











