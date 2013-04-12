from django.conf.urls import patterns, url
from cascade.apps.cartmanager.views import CartUploadView, DataErrorsView, CustomerUploadView, TicketSearchAPI, TicketsCompletedUploadView, \
      CartProfileAPI, CartSearchAPI, CustomerProfileAPI, LocationSearchAPI, CartSearch, CartProfile, \
      CartStatusAPI, CartTypeAPI, TicketSearchAPI, TicketReport, TicketNew, TicketOpen, CustomerReport, CartReport, TicketAPI,\
      CartProfileMap, LocationSearch, CartAddressChange, LocationProfileAPI, CustomerProfile, CustomerNew, AdminDefaultLocation

from rest_framework.urlpatterns import format_suffix_patterns



#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cascade.apps.cartmanager.views',
    url(r'^api/location/profile/(?P<location_id>[a-zA-Z0-9]+)?$', LocationProfileAPI.as_view(), name='location_api_profile'),
    url(r'^api/default/location/$', AdminDefaultLocation.as_view(), name='admin_api_location'),
    url(r'^app/cart/search/$', CartSearch.as_view(), name='cart_search'),
    url(r'^api/cart/search/$', CartSearchAPI.as_view(), name='cart_api_search'),
    url(r'^api/cart/report/$', CartReport.as_view(), name='cart_app_report'),
    url(r'^app/cart/profile/update/location/(?P<serial_number>[a-zA-Z0-9]+)?$', CartAddressChange.as_view(), name='cart_app_address_change'),
    url(r'^app/cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfile.as_view(), name='cart_app_profile'),
    url(r'^app/cart/profile/map/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfileMap.as_view(), name='cart_app_profile_map'),
    url(r'^api/cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfileAPI.as_view(), name='cart_api_profile'),
    url(r'^api/cart/type/options/$', CartTypeAPI.as_view(), name='cart_type_api' ),
    url(r'^api/customer/profile/(?P<customer_id>[a-zA-Z0-9]+)?$',  CustomerProfileAPI.as_view(), name='customer_api_profile'),
    url(r'^app/customer/profile/(?P<customer_id>[a-zA-Z0-9]+)?$',  CustomerProfile.as_view(), name='customer_app_profile'),
    url(r'^app/customer/new/$',  CustomerNew.as_view(), name='customer_app_new'),
    url(r'^app/customer/report/$',  CustomerReport.as_view(), name='customer_app_report'),
    url(r'^api/location/search/$', LocationSearchAPI.as_view(), name='location_api_search'),
    url(r'^app/location/search/$', LocationSearch.as_view(), name='location_app_search'),
    url(r'^api/status/options/$', CartStatusAPI.as_view(), name='cart_status_api' ),
    url(r'^upload/carts/$', CartUploadView.as_view(), name='cart_uploads'),
    url(r'^upload/errors/', DataErrorsView.as_view(), name='upload_errors'),
    url(r'^upload/customers/', CustomerUploadView.as_view(), name='customer_uploads'),
    url(r'^upload/tickets/completed/', TicketsCompletedUploadView.as_view(), name='tickets_completed_upload' ),
    url(r'^api/report/tickets/$', TicketSearchAPI.as_view(), name='tickets_api_download'),
    url(r'^api/ticket/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketAPI.as_view(), name='ticket_api'),
    url(r'^app/tickets/report/$', TicketReport.as_view(), name='ticket_app_report'),
    url(r'^app/tickets/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketNew.as_view(), name='ticket_app_new'),
    url(r'^app/tickets/open/$', TicketOpen.as_view(), name='ticket_app_open'),

 )
urlpatterns = format_suffix_patterns(urlpatterns)
