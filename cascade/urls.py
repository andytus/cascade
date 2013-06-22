from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()

admin.autodiscover()

urlpatterns = patterns('',


    (r'^carts/', include('cascade.apps.cartmanager.urls')),

    url(r'^about/', TemplateView.as_view(template_name="about.html") ),

    url(r'accounts/profile/', TemplateView.as_view(template_name="profile.html")),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),

    url(r'^accounts/register/$', 'cascade.libs.views.register_user'),

    url(r'^accounts/register/success/$', 'cascade.libs.views.register_success'),

)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),

)