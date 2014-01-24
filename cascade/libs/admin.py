__author__ = 'jbennett'
from django.contrib.sites.models import get_current_site
from django.contrib import admin


class SiteAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(SiteAdmin, self).queryset(request)
        return qs.filter(site=get_current_site(request))

