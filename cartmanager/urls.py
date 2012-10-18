from django.conf.urls import patterns, url
from views import CartUploadView, DataErrorsView
from django.views.generic import TemplateView


urlpatterns = patterns('cartmanager.views',
    url(r'^upload/$', CartUploadView.as_view(), name='cart-uploads'),
    url(r'^upload/errors/', DataErrorsView.as_view(), name='upload-errors'),
)

