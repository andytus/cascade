from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from cascade.apps.cartmanager.views import CartUploadView, DataErrorsView, CustomerUploadView, \
    TicketsCompletedUploadView, CartSearch, CartProfile, TicketReport, TicketNew, TicketProfile, \
    CustomerReport, CartReport, LocationSearch, CustomerProfile, CustomerNew,  FileUploadListView, \
    CartAddressChange, CartNew, RouteUploadView

#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cascade.apps.cartmanager.views',
                       url(r'^cart/search/$', CartSearch.as_view(), name='cart_search'),
                       url(r'^cart/report/$', CartReport.as_view(), name='cart_app_report'),
                       url(r'^cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfile.as_view(),
                           name='cart_app_profile'),
                       url(r'^cart/new/(?P<serial_number>[a-zA-Z0-9]+)?$', CartNew.as_view(), name='cart_app_new'),
                       url(r'^cart/profile/update/location/(?P<serial_number>[a-zA-Z0-9]+)?$',
                           CartAddressChange.as_view(), name='cart_app_address_change'),
                       url(r'^customer/profile/(?P<customer_id>[a-zA-Z0-9]+)?$', CustomerProfile.as_view(),
                           name='customer_app_profile'),
                       url(r'^customer/new/$', CustomerNew.as_view(), name='customer_app_new'),
                       url(r'^customer/report/$', CustomerReport.as_view(), name='customer_app_report'),
                       url(r'^location/search/$', LocationSearch.as_view(), name='location_app_search'),
                       url(r'^upload/files/$', FileUploadListView.as_view(), name='upload_file_list'),
                       url(r'^tickets/report/$', TicketReport.as_view(), name='ticket_app_report'),
                       #TODO need to make this view cleaner (like the cart new)
                       url(r'^tickets/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketNew.as_view(), name='ticket_app_new'),
                       url(r'^tickets/profile/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketProfile.as_view(),
                           name='ticket_app_profile'),
                       url(r'^upload/routes/$', RouteUploadView.as_view(), name='route_uploads'),
                       url(r'^upload/carts/$', CartUploadView.as_view(), name='cart_uploads'),
                       url(r'^upload/errors/', DataErrorsView.as_view(), name='upload_errors'),
                       url(r'^upload/customers/', CustomerUploadView.as_view(), name='customer_uploads'),
                       url(r'^upload/tickets/completed/', TicketsCompletedUploadView.as_view(),
                           name='tickets_completed_upload')

                       )

urlpatterns = format_suffix_patterns(urlpatterns)
