from django.conf.urls import patterns, url
from views import CartUploadView, DataErrorsView, CustomerUploadView, TicketsDownloadView, TicketsCompletedUploadView, \
      CartProfileAPI, CartSearchAPI, CustomerProfileAPI, LocationProfileAPI, UpdateCartLocationAPI, CartSearch, CartProfile

#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cartmanager.views',
    url(r'^app/cart/search/$', CartSearch.as_view(), name='cart_search'),
    url(r'^api/cart/search/$', CartSearchAPI.as_view(), name='cart_api_search'),
    url(r'^app/cart/profile/(?P<pk>\d+)?$', CartProfile.as_view(), name='cart_app_profile'),
    url(r'^api/cart/profile/(?P<pk>\d+)?$', CartProfileAPI.as_view(), name='cart_api_profile'),
    url(r'^api/cart/edit_location/(?P<pk>\d+)/$', UpdateCartLocationAPI.as_view(), name='cart_api_change_location'),
    url(r'^api/customer/profile/(?P<pk>\d+)/$',  CustomerProfileAPI.as_view(), name='customer_api_profile'),
    url(r'^app/customer/profile/(?:/(?P<pk>\d+))?$',  CustomerProfileAPI.as_view(), name='customer_app_profile'),
    url(r'^api/location/profile/(?P<pk>\d+)/$', LocationProfileAPI.as_view(), name='location_api_profile'),
    url(r'^app/location/profile/(?:/(?P<pk>\d+))?$', CartProfileAPI.as_view(), name='location_app_profile'),
    url(r'^upload/carts/$', CartUploadView.as_view(), name='cart_uploads'),
    url(r'^upload/errors/', DataErrorsView.as_view(), name='upload_errors'),
    url(r'^upload/customers/', CustomerUploadView.as_view(), name='customer_uploads'),
    url(r'^upload/tickets/completed/', TicketsCompletedUploadView.as_view(), name='tickets_completed_upload' ),
    url(r'^download/tickets/(?P<status>\w+)/(?P<cart_type>\w+)/(?P<service_type>\w+)/$', TicketsDownloadView.as_view(), name='ticket_downloads'),
 )

