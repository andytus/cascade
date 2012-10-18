from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.shortcuts import render_to_response, render
from models import Cart, CartsUploadFile, CartsUploadFileForm, DataErrors
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



class CartUploadView(FormView):
    template_name = 'cartupload.html'
    form_class = CartsUploadFileForm

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        upload_file = CartsUploadFile()
        cart_file = self.request.FILES['cart_file']
        if cart_file.content_type == "application/vnd.ms-excel":
            upload_file.file_path = cart_file
            upload_file.size = cart_file.size
            upload_file.file_kind = 'Carts'
            upload_file.save()
            total_count, good_count, error_count = upload_file.process()
            context['total_count'] = total_count
            context['good_count'] = good_count
            context['error_count'] = error_count
            context['form'] = self.form_class
            context['completed'] = True
            return self.render_to_response(context)

class CustomerUploadView(FormView):
    pass









