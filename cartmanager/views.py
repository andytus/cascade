from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.shortcuts import render_to_response, render
from models import Cart, CartsUploadFile, CartsUploadFileForm
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse


def uploadprocessed(request):
    return HttpResponse("hello")



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
            upload_file.save()
            total_count, error_count, good_count  = upload_file.process()
            context['total_count'] = total_count
            context['good_count'] = good_count
            context['error_count'] = error_count
            context['form'] = self.form_class
            context['completed'] = True
            return self.render_to_response(context)
        #return super(CartUploadView, self).form_valid(form)



#
#
#def get_context_data(self, **kwargs):
#        context = super(CartUploadView, self).get_context_data(**kwargs)
#        context['total_count'] = 0
#        return context
#
#    def get_success_url(self):
#        return reverse('uploadcomplete')
#
#    def form_valid(self, form):
#        upload_file = CartsUploadFile()
#        cart_file = self.request.FILES['cart_file']
#
#        if cart_file.content_type == "application/vnd.ms-excel":
#            upload_file.file_path = cart_file
#            upload_file.size = cart_file.size
#            upload_file.save()
#            total_count, error_count, good_count  = upload_file.process()
#            self.get_success_url()
#
#
#
#
#
#        return super(CartUploadView, self).form_valid(form)



class CustomerUploadView(FormView):
    pass









