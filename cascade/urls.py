from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from cascade.apps.accounts.forms import CustomEditProfileForm
from settings import common as settings

from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()

admin.autodiscover()

urlpatterns = patterns('',

                       (r'^carts/', include('cascade.apps.cartmanager.urls')),

                       (r'^api/', include('cascade.apps.api.urls')),

                       url(r'^about/', TemplateView.as_view(template_name="about.html")),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),


                       url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
                           'userena.views.profile_edit',
                           {'edit_profile_form': CustomEditProfileForm},
                           name='userena_profile_edit'),

                       (r'^accounts/', include('userena.urls')),

                       url(r'^report_builder/', include('cascade.apps.report_builder.urls')),

                       url(r'^api/token/$', 'rest_framework.authtoken.views.obtain_auth_token'),


                       # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       #
                       # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),
                       #
                       # url(r'^accounts/register/$', 'cascade.libs.views.register_user'),
                       #
                       # url(r'^accounts/register/success/$', 'cascade.libs.views.register_success'),

)

urlpatterns += patterns('',
                        (r'^django-rq/', include('django_rq.urls')), )

if settings.DEBUG:
# static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}),
                            (r'^404/$', TemplateView.as_view(template_name="404.html"))
                            )
