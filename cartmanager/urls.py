from django.conf.urls import patterns, include, url
from views import CartUploadView


urlpatterns = patterns('cartmanager.views',
    # Upload carts data from manufacturing
    url(r'^upload/', CartUploadView.as_view(), name='cartuploads'),
)

