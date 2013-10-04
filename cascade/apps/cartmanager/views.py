from django.utils import simplejson
from django.contrib.sites.models import get_current_site

from django.views.generic import TemplateView, ListView
from django.http import Http404
from django.http import HttpResponse

from django_rq import enqueue
from cascade.libs.uploads import process_upload_records

from cascade.libs.mixins import LoginSiteRequiredMixin
from cascade.apps.cartmanager.models import Cart, CartsUploadFile, CustomersUploadFile, \
    TicketsCompleteUploadFile, RouteUploadFile, DataErrors, Site


class FileUploadListView(LoginSiteRequiredMixin, TemplateView):
    """
    A view for rendering a list of uploaded files page.
    Catches the JSON search parameters from the url, loads into
    a dictionary and returns to context variable.

    """
    template_name = 'uploaded_files.html'

    def get_context_data(self, **kwargs):
        context = super(FileUploadListView, self).get_context_data(**kwargs)
        file_id = self.request.GET.get('file_id', None)
        file_type = self.request.GET.get('file_type', None)
        file_status = self.request.GET.get('file_status', None)

        if file_id:
            context['file_id'] = file_id
        if file_type:
            context['file_type'] = file_type
        if file_status:
            context['file_status'] = file_status

        return context


class CartSearch(LoginSiteRequiredMixin, TemplateView):
    """
    A view for rendering the cart search page.
    Catches the search parameters from the url and places
    them into a returned context variable.

    """
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


class CartNew(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_new.html'


class CartReport(LoginSiteRequiredMixin, TemplateView):
    template_name = 'cart_report.html'


class LocationSearch(LoginSiteRequiredMixin, TemplateView):
    template_name = 'location_search.html'

    def get_context_data(self, **kwargs):
        context = super(LocationSearch, self).get_context_data(**kwargs)
        context['address_id'] = self.request.GET.get('address_id', None)
        return context


class CustomerProfile(LoginSiteRequiredMixin, TemplateView):
    template_name = 'customer_profile.html'

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


class DataErrorsView(ListView):
    template_name = 'uploaderrors.html'
    context_object_name = "data_errors"
    queryset = DataErrors.on_site.filter(fix_date__isnull=True)
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(DataErrorsView, self).get_context_data(**kwargs)
        return context


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
        context['file_type'] = self.KIND
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        #TODO implement processing option
        #TODO for now it is just True
        process = request.POST.get('process', True)
        self.get_context_data(**kwargs)
        upload_file = self.MODEL()
        file = self.request.FILES['upload_file']
        #looks for csv type file
        if file.content_type == "application/vnd.ms-excel" or "text/csv":
            upload_file.file_path = file
            upload_file.size = file.size
            upload_file.records_processed = False
            upload_file.file_kind = self.KIND
            upload_file.status = 'UPLOADED'
            upload_file.site = Site.objects.get(id=get_current_site(self.request).id)
            upload_file.uploaded_by = self.request.user
            upload_file.save()
            #Here the records are processed
            if process:
                enqueue(func=process_upload_records, args=(self.MODEL, upload_file.id))
            return HttpResponse(simplejson.dumps({'details': {'message': "Saved %s" % self.FILE,
                                                              'file_id': upload_file.id, 'message_type': 'Success'}}),
                                content_type="application/json")


class CartUploadView(UploadFormView):
    MODEL = CartsUploadFile
    FILE = 'cart_file'
    KIND = 'Carts'
    LINK = 'Cart File Upload'


class CustomerUploadView(UploadFormView):
    MODEL = CustomersUploadFile
    FILE = 'customer_file'
    KIND = 'Customers'
    LINK = 'Customer File Upload'


class TicketsCompletedUploadView(UploadFormView):
    MODEL = TicketsCompleteUploadFile
    FILE = 'ticket_file'
    KIND = 'Tickets'
    LINK = 'Ticket Upload'


class RouteUploadView(UploadFormView):
    MODEL = RouteUploadFile
    FILE = 'route_file'
    KIND = 'Route'
    LINK = 'Route File Upload'
