from django.conf.urls import patterns, url
from cascade.apps.cartmanager.views import CartUploadView, DataErrorsView, CustomerUploadView, TicketDownloadAPI, TicketsCompletedUploadView, \
      CartProfileAPI, CartSearchAPI, CustomerProfileAPI, LocationProfileAPI, UpdateCartLocationAPI, CartSearch, CartProfile, \
      CartStatusAPI, CartTypeAPI
from rest_framework.urlpatterns import format_suffix_patterns

#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cascade.apps.cartmanager.views',
    url(r'^app/cart/search/$', CartSearch.as_view(), name='cart_search'),
    url(r'^api/cart/search/$', CartSearchAPI.as_view(), name='cart_api_search'),
    url(r'^app/cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfile.as_view(), name='cart_app_profile'),
    url(r'^api/cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfileAPI.as_view(), name='cart_api_profile'),
    url(r'^api/cart/edit_location/(?P<pk>\d+)/$', UpdateCartLocationAPI.as_view(), name='cart_api_change_location'),
    url(r'^api/cart/type/options/$', CartTypeAPI.as_view(), name='cart_type_api' ),
    url(r'^api/customer/profile/(?P<pk>\d+)/$',  CustomerProfileAPI.as_view(), name='customer_api_profile'),
    url(r'^app/customer/profile/(?:/(?P<pk>\d+))?$',  CustomerProfileAPI.as_view(), name='customer_app_profile'),
    url(r'^api/location/profile/(?P<pk>\d+)/$', LocationProfileAPI.as_view(), name='location_api_profile'),
    url(r'^app/location/profile/(?:/(?P<pk>\d+))?$', CartProfileAPI.as_view(), name='location_app_profile'),
    url(r'^api/status/options/$', CartStatusAPI.as_view(), name='cart_status_api' ),
    url(r'^upload/carts/$', CartUploadView.as_view(), name='cart_uploads'),
    url(r'^upload/errors/', DataErrorsView.as_view(), name='upload_errors'),
    url(r'^upload/customers/', CustomerUploadView.as_view(), name='customer_uploads'),
    url(r'^upload/tickets/completed/', TicketsCompletedUploadView.as_view(), name='tickets_completed_upload' ),
    url(r'^api/download/tickets/$', TicketDownloadAPI.as_view(), name='tickets_api_download'),
 )

urlpatterns = format_suffix_patterns(urlpatterns)
