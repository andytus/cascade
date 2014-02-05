from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
import json as simplejson
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from cascade.apps.report_builder.models import Report, DisplayField, FilterField, Format, ReportFiles
from cascade.apps.report_builder.utils import javascript_date_format, duplicate, get_model_from_path_string, \
    report_to_list
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django import forms
import datetime
import inspect
import copy
from django_rq import enqueue


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'root_model']

class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'distinct', 'description',]
        widgets = {
            'description': forms.TextInput(
                attrs={'style': 'width:99%;', 'placeholder': 'Description'}),
        }

class DisplayFieldForm(forms.ModelForm):
    class Meta:
        model = DisplayField
        fields = ('name', 'path', 'path_verbose', 'field_verbose', 'field', 'position',
                  'width', 'total', 'sort', 'aggregate', 'group', 'display_format')
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
            'width': forms.TextInput(attrs={'class':'small_input'}),
            'total': forms.CheckboxInput(attrs={'class':'small_input'}),
            'sort': forms.TextInput(attrs={'class':'small_input'}),
        }


class FilterFieldForm(forms.ModelForm):
    class Meta:
        model = FilterField
        fields = ('path', 'path_verbose', 'field_verbose', 'field', 'filter_type',
                 'filter_value', 'filter_value2', 'exclude', 'position')
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly':'readonly'}),
            'field': forms.HiddenInput(),
            'filter_type': forms.Select(attrs={'onchange':'check_filter_type(event.target)'})
        }

    def __init__(self, *args, **kwargs):
        super(FilterFieldForm, self).__init__(*args, **kwargs)
        # override the filter_value field with the models native ChoiceField
        if self.instance.choices:
            self.fields['filter_value'].widget = forms.Select(choices=self.instance.choices)
        if 'DateField' in self.instance.field_verbose or 'DateTimeField' in self.instance.field_verbose:
            widget = self.fields['filter_value'].widget
            widget.attrs['class'] = 'datepicker'
            widget.attrs['data-date-format'] = javascript_date_format(settings.DATE_FORMAT)


class ReportCreateView(CreateView):
    form_class = ReportForm
    template_name = 'report_new.html'


def get_relation_fields_from_model(model_class):
    relation_fields = []
    all_fields_names = model_class._meta.get_all_field_names()
    for field_name in all_fields_names:
        field = model_class._meta.get_field_by_name(field_name)
        if field[3] or not field[2] or hasattr(field[0], 'related'):
            field[0].field_name = field_name
            relation_fields += [field[0]]
    return relation_fields

def get_direct_fields_from_model(model_class):
    direct_fields = []
    all_fields_names = model_class._meta.get_all_field_names()
    for field_name in all_fields_names:
        field = model_class._meta.get_field_by_name(field_name)
        # Direct, not m2m, not FK
        if field[2] and not field[3] and field[0].__class__.__name__ != "ForeignKey":
            direct_fields += [field[0]]
    return direct_fields

def get_custom_fields_from_model(model_class):
    """ django-custom-fields support
    """
    if 'custom_field' in settings.INSTALLED_APPS:
        from custom_field.models import CustomField
        try:
            content_type = ContentType.objects.get(model=model_class._meta.module_name,app_label=model_class._meta.app_label)
        except ContentType.DoesNotExist:
            content_type = None
        custom_fields = CustomField.objects.filter(content_type=content_type)
        return custom_fields

def isprop(v):
    return isinstance(v, property)

def get_properties_from_model(model_class):
    properties = []
    attr_names = [name for (name, value) in inspect.getmembers(model_class, isprop)]
    for attr_name in attr_names:
        if attr_name.endswith('pk'):
            attr_names.remove(attr_name)
        else:
            properties.append(dict(label=attr_name, name=attr_name.strip('_').replace('_',' ')))
    return sorted(properties, key=lambda k: k['label'])


@staff_member_required
def ajax_get_related(request):
    """ Get related model and fields
    Requires get variables model and field
    Returns the model the field belongs to
    """
    field_name = request.GET['field']
    model = ContentType.objects.get(pk=request.GET['model']).model_class()
    field = model._meta.get_field_by_name(field_name)
    path = request.GET['path']
    path_verbose = request.GET['path_verbose']

    if field[2]:
        # Direct field
        new_model = field[0].related.parent_model()
    else:
        # Indirect related field
        new_model = field[0].model()

    new_fields = get_relation_fields_from_model(new_model)
    model_ct = ContentType.objects.get_for_model(new_model)

    if path_verbose:
        path_verbose += "::"
    path_verbose += field[0].name

    path += field_name
    path += '__'

    return render_to_response('report_builder/report_form_related_li.html', {
        'model_ct': model_ct,
        'related_fields': new_fields,
        'path': path,
        'path_verbose': path_verbose,
    }, RequestContext(request, {}),)

def fieldset_string_to_field(fieldset_dict, model):
    if isinstance(fieldset_dict['fields'], tuple):
        fieldset_dict['fields'] = list(fieldset_dict['fields'])
    i = 0
    for dict_field in fieldset_dict['fields']:
        if isinstance(dict_field, basestring):
            fieldset_dict['fields'][i] = model._meta.get_field_by_name(dict_field)[0]
        elif isinstance(dict_field, list) or isinstance(dict_field, tuple):
            dict_field[1]['recursive'] = True
            fieldset_string_to_field(dict_field[1], model)
        i += 1

def get_fieldsets(model):
    """ fieldsets are optional, they are defined in the Model.
    """
    fieldsets = getattr(model, 'report_builder_fieldsets', None)
    if fieldsets:
        for fieldset_name, fieldset_dict in model.report_builder_fieldsets:
            fieldset_string_to_field(fieldset_dict, model)
    return fieldsets

@staff_member_required
def ajax_get_fields(request):
    """ Get fields and properties for a particular model
    """
    field_name = request.GET.get('field')
    model = ContentType.objects.get(pk=request.GET['model']).model_class()
    path = request.GET['path']
    path_verbose = request.GET.get('path_verbose')
    properties = get_properties_from_model(model)
    custom_fields = get_custom_fields_from_model(model)
    root_model = model.__name__.lower()
    app_label = model._meta.app_label
    fieldsets = get_fieldsets(model)

    if field_name == '':
        return render_to_response('report_builder/report_form_fields_li.html', {
            'fields': get_direct_fields_from_model(model),
            'fieldsets': fieldsets,
            'properties': properties,
            'custom_fields': custom_fields,
            'root_model': root_model,
            'app_label': app_label,
        }, RequestContext(request, {}),)

    field = model._meta.get_field_by_name(field_name)
    if path_verbose:
        path_verbose += "::"
    # TODO: need actual model name to generate choice list (not pluralized field name)
    # - maybe store this as a separate value?
    if field[3] and hasattr(field[0], 'm2m_reverse_field_name'):
        path_verbose += field[0].m2m_reverse_field_name()
    else:
        path_verbose += field[0].name

    path += field_name
    path += '__'
    if field[2]:
        # Direct field
        new_model = field[0].related.parent_model
        path_verbose = new_model.__name__.lower()
    else:
        # Indirect related field
        new_model = field[0].model
        path_verbose = new_model.__name__.lower()

    fields = get_direct_fields_from_model(new_model)
    if hasattr(new_model, 'report_builder_exclude_fields'):
        good_fields = []
        for field in fields:
            if not field.name in new_model.report_builder_exclude_fields:
                good_fields += [field]
        fields = good_fields


    custom_fields = get_custom_fields_from_model(new_model)
    properties = get_properties_from_model(new_model)
    app_label = new_model._meta.app_label

    return render_to_response('report_builder/report_form_fields_li.html', {
        'fields': fields,
        'fieldsets': fieldsets,
        'custom_fields': custom_fields,
        'properties': properties,
        'path': path,
        'path_verbose': path_verbose,
        'root_model': root_model,
        'app_label': app_label,
    }, RequestContext(request, {}),)

@staff_member_required
def ajax_get_choices(request):
    path_verbose = request.GET.get('path_verbose')
    label = request.GET.get('label')
    root_model = request.GET.get('root_model')
    app_label = request.GET.get('app_label')
    model_name = path_verbose or root_model
    model_name = model_name.split(':')[-1]
    model = ContentType.objects.get(model=model_name, app_label=app_label).model_class()
    choices = FilterField().get_choices(model, label)
    select_widget = forms.Select(choices=[('','---------')] + list(choices))
    options_html = select_widget.render_options([], [0])
    return HttpResponse(options_html)

@staff_member_required
def ajax_get_formats(request):
    choices = Format.objects.values_list('pk', 'name')
    select_widget = forms.Select(choices=[('','---------')] + list(choices))
    options_html = select_widget.render_options([], [0])
    return HttpResponse(options_html)

def sort_helper(x, sort_key, date_field=False):
    # If comparing datefields, assume null is the min year
    if date_field and x[sort_key] == None:
        result = datetime.date(datetime.MINYEAR, 1, 1)
    else:
        result = x[sort_key]
    return result.lower() if isinstance(result, basestring) else result



@staff_member_required
def ajax_preview(request):
    """ This view is intended for a quick preview useful when debugging
    reports. It limits to 50 objects.
    """
    report = get_object_or_404(Report, pk=request.POST['report_id'])
    objects_list, message = report_to_list(report, request.user, preview=True)

    return render_to_response('report_builder/html_report.html', {
        'report': report,
        'objects_dict': objects_list,
        'message': message

    }, RequestContext(request, {}),)

class ReportUpdateView(UpdateView):
    """ This view handles the edit report builder
    It includes attached formsets for display and criteria fields
    """
    model = Report
    form_class = ReportEditForm
    success_url = './'

    @method_decorator(permission_required('report_builder.change_report'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReportUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ReportUpdateView, self).get_context_data(**kwargs)
        model_class = self.object.root_model.model_class()
        model_ct = ContentType.objects.get_for_model(model_class)
        properties = get_properties_from_model(model_class)
        custom_fields = get_custom_fields_from_model(model_class)

        direct_fields = get_direct_fields_from_model(model_class)
        relation_fields = get_relation_fields_from_model(model_class)

        DisplayFieldFormset = inlineformset_factory(
            Report,
            DisplayField,
            extra=0,
            can_delete=True,
            form=DisplayFieldForm)

        FilterFieldFormset = inlineformset_factory(
            Report,
            FilterField,
            extra=0,
            can_delete=True,
            form=FilterFieldForm)

        if self.request.POST:
            ctx['field_list_formset'] =  DisplayFieldFormset(self.request.POST, instance=self.object)
            ctx['field_filter_formset'] =  FilterFieldFormset(self.request.POST, instance=self.object, prefix="fil")
        else:
            ctx['field_list_formset'] =  DisplayFieldFormset(instance=self.object)
            ctx['field_filter_formset'] =  FilterFieldFormset(instance=self.object, prefix="fil")

        ctx['related_fields'] = relation_fields
        ctx['fields'] = direct_fields
        ctx['fieldsets'] = get_fieldsets(model_class)
        ctx['custom_fields'] = custom_fields
        ctx['properties'] = properties
        ctx['model_ct'] = model_ct
        ctx['root_model'] = model_ct.model
        ctx['app_label'] = model_ct.app_label

        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        field_list_formset = context['field_list_formset']
        field_filter_formset = context['field_filter_formset']

        if field_list_formset.is_valid() and field_filter_formset.is_valid():
            self.object = form.save()
            field_list_formset.report = self.object
            field_list_formset.save()
            field_filter_formset.report = self.object
            field_filter_formset.save()
            self.object.check_report_display_field_positions()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class FileIterWrapper(object):
    def __init__(self, flo, chunk_size = 1024**2):
        self.flo = flo
        self.chunk_size = chunk_size

    def next(self):
        data = self.flo.getvalue(self.chunk_size)
        if data:
            print data
            return data
        else:
            raise StopIteration

    def __iter__(self):
        return self

@staff_member_required
def download_xlsx(request, pk, queryset=None):
    """ Download the full report in xlsx format
    Why xlsx? Because there is no decent ods library for python and xls has limitations
    queryset: predefined queryset to bypass filters
    """
    report = get_object_or_404(Report, pk=pk)
    report_file = ReportFiles.objects.get(site=get_current_site(request), report=report, file_extension='xlsx')
    if report_file.file_path:
        response = HttpResponse(report_file.file_path,
                  content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s.%s' % (report.name, report_file.file_extension)
        return response
    else:
        raise Http404

@staff_member_required
def ajax_add_star(request, pk):
    """ Star or unstar report for user
    """
    report = get_object_or_404(Report, pk=pk)
    user = request.user
    if user in report.starred.all():
        added = False
        report.starred.remove(request.user)
    else:
        added = True
        report.starred.add(request.user)
    return HttpResponse(added)

@staff_member_required
def create_copy(request, pk):
    """ Copy a report including related fields """
    report = get_object_or_404(Report, pk=pk)
    new_report = duplicate(report, changes=(
        ('name', '{0} (copy)'.format(report.name)),
        ('user_created', request.user),
        ('user_modified', request.user),
    ))
    # duplicate does not get related
    for display in report.displayfield_set.all():
        new_display = copy.copy(display)
        new_display.pk = None
        new_display.report = new_report
        new_display.save()
    for report_filter in report.filterfield_set.all():
        new_filter = copy.copy(report_filter)
        new_filter.pk = None
        new_filter.report = new_report
        new_filter.save()
    return redirect(new_report)


@staff_member_required
def export_to_report(request):
    """ Export objects (by ID and content type) to an existing or new report
    In effect this runs the report with it's display fields. It ignores
    filters and filters instead the provided ID's. It can be select
    as a global admin action.
    """
    admin_url = request.GET.get('admin_url', '/')
    ct = ContentType.objects.get_for_id(request.GET['ct'])
    ids = request.GET['ids'].split(',')
    number_objects = len(ids)
    reports = Report.objects.filter(root_model=ct).order_by('-modified')

    if 'download' in request.GET:
        report = get_object_or_404(Report, pk=request.GET['download'])
        queryset = ct.model_class().objects.filter(pk__in=ids)
        return download_xlsx(request, report.id, queryset=queryset)

    return render(request, 'report_builder/export_to_report.html', {
        'object_list': reports,
        'admin_url': admin_url,
        'number_objects': number_objects,
        'model': ct.model_class()._meta.verbose_name,
        })

@staff_member_required
def generate_reports_admin(request, pk):
    report = Report.objects.get(pk=pk)
    enqueue(func=report.generate_report_sites, args=(request.user,), timeout=50000)
    return redirect('/admin/report_builder/report/')


def generate_report(request, pk):
    report = Report.on_site.get(pk=int(pk))
    generate = request.GET['generate']

    site = get_current_site(request)
    report_file = report.report_file.get(site=site, file_extension='xlsx')
    print report_file.update_in_progress
    if generate == 'true':
        report_file.update_in_progress = 'Yes'
        report_file.save()
        enqueue(func=report.generate_report, args=(request.user, site), timeout=5000)

    return HttpResponse(simplejson.dumps({'last_generated':report_file.last_generated.strftime('%Y-%m-%d %H:%M'),
                                          'update_in_progress': report_file.update_in_progress
                                         }), content_type="application/json")