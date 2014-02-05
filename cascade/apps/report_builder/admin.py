from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from cascade.apps.report_builder.models import DisplayField, Report, FilterField, Format
from django.conf import settings
from cascade.libs.admin import SiteAdmin
from django.utils.safestring import mark_safe
from django_rq import enqueue

static_url = getattr(settings, 'STATIC_URL', '/static/')

class StarredFilter(SimpleListFilter):
    title = 'Your starred reports'
    parameter_name = 'starred'
    def lookups(self, request, model_admin):
        return (
            ('Starred', 'Starred Reports'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'Starred':
            return queryset.filter(starred=request.user)

class ReportAdmin(SiteAdmin):
    list_display = ('ajax_starred', 'edit', 'name', 'description', 'root_model', 'created', 'modified', 'user_created',
                    'download_xlsx','copy_report', "run_report_generate", 'last_generated')
    readonly_fields = ['slug']
    fields = ['name', 'description', 'root_model', 'slug', 'site']
    search_fields = ('name', 'description')
    list_filter = (StarredFilter, 'root_model', 'created', 'modified', 'root_model__app_label')
    list_display_links = ['name']
    actions = ['generate_reports_action']

    class Media:
        js = [static_url+'report_builder/js/jquery-1.8.2.min.js', static_url+'report_builder/js/report_list.js',]

    def generate_reports_action(self, request, queryset):
        for obj in queryset:
            enqueue(func=obj.generate_report_sites, args=(request.user,), timeout=50000)
        self.message_user(request, "Generating reports now: (may take a while depending on amount of data and sites)")
    generate_reports_action.short_description = "Generate reports for all sites"

    def last_generated(self, obj):
        #grab the last file generated and present as last_generated
        generated = obj.report_file.all().order_by('-last_generated')
        if generated.count() > 0:
            last_generated = generated[0].last_generated
            return last_generated
        else:
            return "No Files"

    def download_xlsx(self, obj):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/download.svg"/></a>'.format(
            reverse('cascade.apps.report_builder.views.download_xlsx', args=[obj.id]),
            getattr(settings, 'STATIC_URL', '/static/'),
        ))
    download_xlsx.short_description = "Download"
    download_xlsx.allow_tags = True

    def edit(self, obj):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin: '
                         '-6px" src="{1}report_builder/img/edit.svg"/></a>'.format(
            obj.get_absolute_url(), getattr(settings, 'STATIC_URL', '/static/')
        ))
    edit.allow_tags = True

    def run_report_generate(self, obj):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin -6px" '
                         'src="{1}report_builder/img/refresh-icon.png"/></a>'.format(
                          reverse('cascade.apps.report_builder.views.generate_reports_admin', args=[obj.id]),
                          getattr(settings, 'STATIC_URL', '/static/'),
        ))
    run_report_generate.short_description = "Generate"
    run_report_generate.allow_tags = True

    def copy_report(self, obj):
        return '<a href="{0}"><img style="width: 26px; margin: -6px" ' \
               'src="{1}report_builder/img/copy.svg"/></a>'.format(
               reverse('cascade.apps.report_builder.views.create_copy', args=[obj.id]),
               getattr(settings, 'STATIC_URL', '/static/'),
        )
    copy_report.short_description = "Copy"
    copy_report.allow_tags = True

    def response_add(self, request, obj, post_url_continue=None):
        if '_easy' in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(ReportAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_easy' in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(ReportAdmin, self).response_change(request, obj)

    def changelist_view(self, request, extra_context=None):
        self.user = request.user
        return super(ReportAdmin, self).changelist_view(request, extra_context=extra_context)

    def ajax_starred(self, obj):
        if obj.starred.filter(id=self.user.id):
            img = static_url+'report_builder/img/star.png'
        else:
            img = static_url+'report_builder/img/unstar.png'
        return '<a href="javascript:void(0)" onclick="ajax_add_star(this, \'{0}\')"><img style="width: 26px; margin: -6px;" src="{1}"/></a>'.format(
            reverse('cascade.apps.report_builder.views.ajax_add_star', args=[obj.id]),
            img)
    ajax_starred.allow_tags = True
    ajax_starred.short_description = "Starred"

    def save_model(self, request, obj, form, change):
        star_user = False
        if not obj.id:
            obj.user_created = request.user
            star_user = True
        obj.user_modified = request.user
        if obj.distinct == None:
            obj.distinct = False
        obj.save()
        if star_user: # Star created reports automatically
            obj.starred.add(request.user)

admin.site.register(Report, ReportAdmin)
admin.site.register(Format)

def export_to_report(modeladmin, request, queryset):
    admin_url = request.get_full_path()
    selected_int = queryset.values_list('id', flat=True)
    selected = []
    for s in selected_int:
        selected.append(str(s))
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect(reverse('cascade.apps.report_builder.views.export_to_report') + "?ct=%s&admin_url=%s&ids=%s" % (ct.pk, admin_url, ",".join(selected)))

if getattr(settings, 'REPORT_BUILDER_GLOBAL_EXPORT', False):
    admin.site.add_action(export_to_report, 'Export to Report')
