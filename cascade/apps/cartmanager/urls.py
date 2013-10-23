from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from cascade.apps.cartmanager.views import CartUploadView, DataErrorsView, CustomerUploadView, \
    TicketsCompletedUploadView, CartSearch, CartProfile, TicketReport, TicketNew, TicketProfile, \
    CustomerReport, CartReport, LocationSearch, CustomerProfile, CustomerNew,  FileUploadListView, \
    CartAddressChange, CartNew, RouteUploadView, GetUploadTemplate

from django.views.decorators.cache import cache_page

#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cascade.apps.cartmanager.views',
                       url(r'^cart/search/$',
                           cache_page(60 * 3)(CartSearch.as_view()), name='cart_search'),
                       url(r'^cart/report/$',
                           cache_page(60 * 3)(CartReport.as_view()), name='cart_app_report'),
                       url(r'^cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$',
                           cache_page(60 * 3)(CartProfile.as_view()),
                           name='cart_app_profile'),
                       url(r'^cart/new/(?P<serial_number>[a-zA-Z0-9]+)?$',
                           cache_page(60 * 3)(CartNew.as_view()), name='cart_app_new'),
                       url(r'^cart/profile/update/location/(?P<serial_number>[a-zA-Z0-9]+)?$',
                           CartAddressChange.as_view(), name='cart_app_address_change'),
                       url(r'^customer/profile/(?P<customer_id>[a-zA-Z0-9]+)?$',
                           cache_page(60 * 3)(CustomerProfile.as_view()),
                           name='customer_app_profile'),
                       url(r'^customer/new/$', cache_page(60 * 3)(CustomerNew.as_view()), name='customer_app_new'),
                       url(r'^customer/report/$',
                           cache_page(60 * 3)(CustomerReport.as_view()), name='customer_app_report'),
                       url(r'^location/search/$',
                           cache_page(60 * 3)(LocationSearch.as_view()), name='location_app_search'),
                       url(r'^upload/files/$',
                           cache_page(60 * 3)(FileUploadListView.as_view()), name='upload_file_list'),
                       url(r'^tickets/report/$',
                           cache_page(60 * 3)(TicketReport.as_view()), name='ticket_app_report'),
                       #TODO need to make this view cleaner (like the cart new)
                       url(r'^tickets/(?P<ticket_id>[a-zA-Z0-9]+)?$',
                           cache_page(60 * 3)(TicketNew.as_view()), name='ticket_app_new'),
                       url(r'^tickets/profile/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketProfile.as_view(),
                           name='ticket_app_profile'),
                       url(r'^upload/routes/$',
                           cache_page(60 * 3)(RouteUploadView.as_view()), name='route_uploads'),
                       url(r'^upload/carts/$',
                           cache_page(60 * 3)(CartUploadView.as_view()), name='cart_uploads'),
                       url(r'^upload/errors/',
                           cache_page(60 * 3)(DataErrorsView.as_view()), name='upload_errors'),
                       url(r'^upload/customers/',
                           cache_page(60 * 3)(CustomerUploadView.as_view()), name='customer_uploads'),
                       url(r'^upload/tickets/completed/',
                           cache_page(60 * 3)(TicketsCompletedUploadView.as_view()),
                           name='tickets_completed_upload'),
                       url(r'^upload/templates/(?P<type>[a-zA-Z0-9]+)?$',
                           cache_page(60 * 3)(GetUploadTemplate.as_view()),
                           name='template_uploads')
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
