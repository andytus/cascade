from django.conf.urls import patterns, url
from cascade.apps.api.views import TicketSearchAPI, CartProfileAPI, CartSearchAPI, CustomerProfileAPI, \
    LocationSearchAPI, CartStatusAPI, CartTypeAPI, TicketAPI, LocationAPI, AdminDefaultLocation, TicketStatusAPI, \
    TicketCommentAPI, TicketServiceTypeAPI, FileUploadListAPI, RouteListAPI

from rest_framework.urlpatterns import format_suffix_patterns

#Note the regex pattern (?:/(?P<pk>\d+)?$ is used to make this optional, added a default view to accommodate.
urlpatterns = patterns('cascade.apps.api.views',
                       url(r'^location/profile/(?P<location_id>[a-zA-Z0-9]+)?$', LocationAPI.as_view(),
                           name='location_api_profile'),
                       url(r'^location/search/$', LocationSearchAPI.as_view(), name='location_api_search'),
                       url(r'^default/location/$', AdminDefaultLocation.as_view(), name='admin_api_location'),
                       url(r'^cart/search/$', CartSearchAPI.as_view(), name='cart_api_search'),
                       url(r'^cart/profile/(?P<serial_number>[a-zA-Z0-9]+)?$', CartProfileAPI.as_view(),
                           name='cart_api_profile'),
                       url(r'^cart/type/options/$', CartTypeAPI.as_view(), name='cart_type_api'),
                       url(r'^cart/status/options/$', CartStatusAPI.as_view(), name='cart_status_api'),
                       url(r'^customer/profile/(?P<customer_id>[a-zA-Z0-9]+)?$', CustomerProfileAPI.as_view(),
                           name='customer_api_profile'),
                       url(r'^upload/files/', FileUploadListAPI.as_view(), name='upload_file_list_api'),
                       url(r'^report/tickets/$', TicketSearchAPI.as_view(), name='tickets_api_download'),
                       url(r'^ticket/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketAPI.as_view(), name='ticket_api'),
                       url(r'^ticket/comment/(?P<ticket_id>[a-zA-Z0-9]+)?$', TicketCommentAPI.as_view(),
                           name='ticket_comment_api'),
                       url(r'^ticket/status/options/$', TicketStatusAPI.as_view(), name='ticket_status_api'),
                       url(r'^ticket/service/options/$', TicketServiceTypeAPI.as_view(),
                           name='ticket_service_type_api'),
                       url(r'^route/search/$', RouteListAPI.as_view(), name='route_search_api')
                       )

urlpatterns = format_suffix_patterns(urlpatterns)

