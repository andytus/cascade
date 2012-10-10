from models import Cart, CartsUploadFile, CartsUploadFileForm
from django.views.generic.edit import FormView


class CartUploadView(FormView):
    template_name = 'cartupload.html'
    form_class =  CartsUploadFileForm
    success_url = '/worked/'

    def form_valid(self, form):
        upload_file = CartsUploadFile()
        cart_file = self.request.FILES['cart_file']

        if cart_file.content_type == "application/vnd.ms-excel":
            upload_file.file_path = cart_file
            upload_file.size = cart_file.size
            upload_file.save()

#            with open(upload_file, 'wb+') as destination:
#                for chunk in cart_file.chunks():
#                    destination.write(chunk)
#            for line in cart_file:
#                print line[0]
        return super(CartUploadView, self).form_valid(form)









