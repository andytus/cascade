__author__ = 'jbennett'


from django.http import Http404
from django.conf import settings
from django.contrib.sites.models import Site


class MultiSiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host().lower()
        try:
            site = Site.objects.get(domain=host)
            settings.SITE_ID = site.pk

        except Site.DoesNotExist:
            #TODO change redirect to generic about page
            raise Http404