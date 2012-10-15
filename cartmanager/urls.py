from django.conf.urls import patterns, url
from views import CartUploadView
from django.views.generic import TemplateView


urlpatterns = patterns('cartmanager.views',
    url(r'^upload/', CartUploadView.as_view(), name='cartuploads'),

)

