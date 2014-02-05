import copy
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor
from django.db.models import Q
from django.views.generic import ListView
import warnings
from numbers import Number
from decimal import Decimal
import time
import re
import datetime
from dateutil import parser

def filter_property(filter_field, value):
    filter_type = filter_field.filter_type
    filter_value = filter_field.filter_value
    filtered = True
    #TODO: i10n
    WEEKDAY_INTS = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }
    #TODO instead of catch all, deal with all cases
    # Example is 'a' < 2 is a valid python comparison
    # But what about 2 < '1' which yeilds true! Not intuitive for humans.
    try:
        if filter_type == 'exact' and str(value) == filter_value:
            filtered = False
        if filter_type == 'iexact' and str(value).lower() == str(filter_value).lower():
            filtered = False
        if filter_type == 'contains' and filter_value in value:
            filtered = False
        if filter_type == 'icontains' and str(filter_value).lower() in str(value).lower():
            filtered = False
        if filter_type == 'in' and value in filter_value:
            filtered = False
        # convert dates and datetimes to timestamps in order to compare digits and date/times the same
        if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
            value = str(time.mktime(value.timetuple()))
            try:
                filter_value_dt = parser.parse(filter_value)
                filter_value = str(time.mktime(filter_value_dt.timetuple()))
            except ValueError:
                pass
        if filter_type == 'gt' and Decimal(value) > Decimal(filter_value):
            filtered = False
        if filter_type == 'gte' and Decimal(value) >= Decimal(filter_value):
            filtered = False
        if filter_type == 'lt' and Decimal(value) < Decimal(filter_value):
            filtered = False
        if filter_type == 'lte' and Decimal(value) <= Decimal(filter_value):
            filtered = False
        if filter_type == 'startswith' and str(value).startswith(str(filter_value)):
            filtered = False
        if filter_type == 'istartswith' and str(value).lower().startswith(str(filter_value)):
            filtered = False
        if filter_type == 'endswith' and str(value).endswith(str(filter_value)):
            filtered = False
        if filter_type == 'iendswith' and str(value).lower().endswith(str(filter_value)):
            filtered = False
        if filter_type == 'range' and value in [int(x) for x in filter_value]:
            filtered = False
        if filter_type == 'week_day' and WEEKDAY_INTS.get(str(filter_value).lower()) == value.weekday:
            filtered = False
        if filter_type == 'isnull' and value == None:
            filtered = False
        if filter_type == 'regex' and re.search(filter_value, value):
            filtered = False
        if filter_type == 'iregex' and re.search(filter_value, value, re.I):
            filtered = False
    except:
        pass

    if filter_field.exclude:
        return not filtered
    return filtered


def javascript_date_format(python_date_format):
    format = python_date_format.replace(r'Y', 'yyyy')
    format = format.replace(r'm', 'mm')
    format = format.replace(r'd', 'dd')
    if not format:
        format = 'yyyy-mm-dd'
    return format

def duplicate(obj, changes=None):
    """ Duplicates any object including m2m fields
    changes: any changes that should occur, example
    changes = (('fullname','name (copy)'), ('do not copy me', ''))"""
    if not obj.pk:
        raise ValueError('Instance must be saved before it can be cloned.')
    duplicate = copy.copy(obj)
    duplicate.pk = None
    for change in changes:
        duplicate.__setattr__(change[0], change[1])
    duplicate.save()
    # trick to copy ManyToMany relations.
    for field in obj._meta.many_to_many:
        source = getattr(obj, field.attname)
        destination = getattr(duplicate, field.attname)
        for item in source.all():
            try: # m2m, through fields will fail.
                destination.add(item)
            except: pass
    return duplicate


def get_model_from_path_string(root_model, path):
    """ Return a model class for a related model
    root_model is the class of the initial model
    path is like foo__bar where bar is related to foo
    """
    for path_section in path.split('__'):
        if path_section:
            field = root_model._meta.get_field_by_name(path_section)
            if field[2]:
                root_model = field[0].related.parent_model()
            else:
                root_model = field[0].model
    return root_model


def sort_helper(x, sort_key, date_field=False):
    # If comparing datefields, assume null is the min year
    if date_field and x[sort_key] == None:
        result = datetime.date(datetime.MINYEAR, 1, 1)
    else:
        result = x[sort_key]
    return result.lower() if isinstance(result, basestring) else result

def report_to_list(report, user, site=None, preview=False, queryset=None):
    """ Create list from a report with all data filtering
    preview: Return only first 50
    objects: Provide objects for list, instead of running filters
    Returns list, message in case of issues
    """
    message= ""
    model_class = report.root_model.model_class()
    if queryset != None:
        objects = report.add_aggregates(queryset)
    else:
        try:
            objects, query_message = report.get_query(site)
            message += query_message
        except exceptions.ValidationError as e:
            message += "Validation Error: {0!s}. Something may be wrong with the report's filters.".format(e)
            return [], message
        except ValueError as e:
            message += "Value Error: {0!s}. Something may be wrong with the report's filters. For example it may be expecting a number but received a character.".format(e)
            return [], message

    # Display Values
    display_field_paths = []
    property_list = {}
    custom_list = {}
    display_totals = {}
    def append_display_total(display_totals, display_field, display_field_key):
        if display_field.total:
            display_totals[display_field_key] = {'val': Decimal('0.00')}


    for i, display_field in enumerate(report.displayfield_set.all()):
        model = get_model_from_path_string(model_class, display_field.path)
        if user.has_perm(model._meta.app_label + '.change_' + model._meta.module_name) \
        or user.has_perm(model._meta.app_label + '.view_' + model._meta.module_name) \
        or not model:
            # TODO: clean this up a bit
            display_field_key = display_field.path + display_field.field
            if '[property]' in display_field.field_verbose:
                property_list[i] = display_field_key
                append_display_total(display_totals, display_field, display_field_key)
            elif '[custom' in display_field.field_verbose:
                custom_list[i] = display_field_key
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Avg":
                display_field_key += '__avg'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Max":
                display_field_key += '__max'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Min":
                display_field_key += '__min'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Count":
                display_field_key += '__count'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            elif display_field.aggregate == "Sum":
                display_field_key += '__sum'
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
            else:
                display_field_paths += [display_field_key]
                append_display_total(display_totals, display_field, display_field_key)
        else:
            message += "You don't have permission to " + display_field.name
    try:
        if user.has_perm(report.root_model.app_label + '.change_' + report.root_model.model) \
        or user.has_perm(report.root_model.app_label + '.view_' + report.root_model.model):

            def increment_total(display_field_key, display_totals, val):
                if display_totals.has_key(display_field_key):
                    # Booleans are Numbers - blah
                    if isinstance(val, Number) and not isinstance(val, bool):
                        # do decimal math for all numbers
                        display_totals[display_field_key]['val'] += Decimal(str(val))
                    else:
                        display_totals[display_field_key]['val'] += Decimal('1.00')


            # get pk for primary and m2m relations in order to retrieve objects
            # for adding properties to report rows
            display_field_paths.insert(0, 'pk')
            m2m_relations = []
            for position, property_path in property_list.iteritems():
                property_root = property_path.split('__')[0]
                root_class = report.root_model.model_class()
                property_root_class = getattr(root_class, property_root)
                if type(property_root_class) == ReverseManyRelatedObjectsDescriptor:
                    display_field_paths.insert(1, '%s__pk' % property_root)
                    m2m_relations.append(property_root)
            values_and_properties_list = []
            filtered_report_rows = []
            group = None
            for df in report.displayfield_set.all():
                if df.group:
                    group = df.path + df.field
                    break
            if group:
                filtered_report_rows = report.add_aggregates(objects.values_list(group))
            else:
                values_list = objects.values_list(*display_field_paths)

            if not group:
                for row in values_list:
                    row = list(row)
                    obj = report.root_model.model_class().objects.get(pk=row.pop(0))
                    #related_objects
                    remove_row = False
                    values_and_properties_list.append(row)
                    # filter properties (remove rows with excluded properties)
                    property_filters = report.filterfield_set.filter(
                        Q(field_verbose__contains='[property]') | Q(field_verbose__contains='[custom')
                        )
                    for property_filter in property_filters:
                        root_relation = property_filter.path.split('__')[0]
                        if root_relation in m2m_relations:
                            pk = row[0]
                            if pk is not None:
                                # a related object exists
                                m2m_obj = getattr(obj, root_relation).get(pk=pk)
                                val = reduce(getattr, [property_filter.field], m2m_obj)
                            else:
                                val = None
                        else:
                            if '[custom' in property_filter.field_verbose:
                                for relation in property_filter.path.split('__'):
                                    if hasattr(obj, root_relation):
                                        obj = getattr(obj, root_relation)
                                val = obj.get_custom_value(property_filter.field)
                            else:
                                val = reduce(getattr, (property_filter.path + property_filter.field).split('__'), obj)
                        if filter_property(property_filter, val):
                            remove_row = True
                            values_and_properties_list.pop()
                            break
                    if not remove_row:
                        # increment totals for fields
                        for i, field in enumerate(display_field_paths[1:]):
                            if field in display_totals.keys():
                                increment_total(field, display_totals, row[i])
                        for position, display_property in property_list.iteritems():
                            relations = display_property.split('__')
                            root_relation = relations[0]
                            if root_relation in m2m_relations:
                                pk = row.pop(0)
                                if pk is not None:
                                    # a related object exists
                                    m2m_obj = getattr(obj, root_relation).get(pk=pk)
                                    val = reduce(getattr, relations[1:], m2m_obj)
                                else:
                                    val = None
                            else:
                                try: # Could error if a related field doesn't exist
                                    val = reduce(getattr, relations, obj)
                                except AttributeError:
                                    val = None
                            values_and_properties_list[-1].insert(position, val)
                            increment_total(display_property, display_totals, val)
                        for position, display_custom in custom_list.iteritems():
                            val = obj.get_custom_value(display_custom)
                            values_and_properties_list[-1].insert(position, val)
                            increment_total(display_custom, display_totals, val)
                        filtered_report_rows += [values_and_properties_list[-1]]
                    if preview and len(filtered_report_rows) == 50:
                        break
            sort_fields = report.displayfield_set.filter(sort__gt=0).order_by('-sort').\
                values_list('position', 'sort_reverse')
            for sort_field in sort_fields:
                try:
                    filtered_report_rows = sorted(
                        filtered_report_rows,
                        key=lambda x: sort_helper(x, sort_field[0]-1),
                        reverse=sort_field[1]
                        )
                except TypeError: # Sorry crappy way to determine if date is being sorted
                    filtered_report_rows = sorted(
                        filtered_report_rows,
                        key=lambda x: sort_helper(x, sort_field[0]-1, date_field=True),
                        reverse=sort_field[1]
                        )
            values_and_properties_list = filtered_report_rows
        else:
            values_and_properties_list = []
            message = "Permission Denied on %s" % report.root_model.name


        # add choice list display and display field formatting
        choice_lists = {}
        display_formats = {}
        final_list = []
        for df in report.displayfield_set.all():
            if df.choices:
                df_choices = df.choices_dict
                # Insert blank and None as valid choices
                df_choices[''] = ''
                df_choices[None] = ''
                choice_lists.update({df.position: df_choices})
            if df.display_format:
                display_formats.update({df.position: df.display_format})

        for row in values_and_properties_list:
            # add display totals for grouped result sets
            # TODO: dry this up, duplicated logic in non-grouped total routine
            if group:
                # increment totals for fields
                for i, field in enumerate(display_field_paths[1:]):
                    if field in display_totals.keys():
                        increment_total(field, display_totals, row[i])
            row = list(row)
            for position, choice_list in choice_lists.iteritems():
                row[position-1] = unicode(choice_list[row[position-1]])
            for position, display_format in display_formats.iteritems():
                # convert value to be formatted into Decimal in order to apply
                # numeric formats
                try:
                    value = Decimal(row[position-1])
                except:
                    value = row[position-1]
                # Try to format the value, let it go without formatting for ValueErrors
                try:
                    row[position-1] = display_format.string.format(value)
                except ValueError:
                    row[position-1] = value
            final_list.append(row)
        values_and_properties_list = final_list


        if display_totals:
            display_totals_row = []

            fields_and_properties = list(display_field_paths[1:])
            for position, value in property_list.iteritems():
                fields_and_properties.insert(position, value)
            for i, field in enumerate(fields_and_properties):
                if field in display_totals.keys():
                    display_totals_row += [display_totals[field]['val']]
                else:
                    display_totals_row += ['']

            # add formatting to display totals
            for df in report.displayfield_set.all():
                if df.display_format:
                    try:
                        value = Decimal(display_totals_row[df.position-1])
                    except:
                        value = display_totals_row[df.position-1]
                    # Fall back to original value if format string and value
                    # aren't compatible, e.g. a numerically-oriented format
                    # string with value which is not numeric.
                    try:
                        value = df.display_format.string.format(value)
                    except ValueError:
                        pass
                    display_totals_row[df.position-1] = value

        if display_totals:
            values_and_properties_list = (
                values_and_properties_list + [
                    ['TOTALS'] + (len(fields_and_properties) - 1) * ['']
                    ] + [display_totals_row]
                )



    except exceptions.FieldError as e:
        warnings.warn('Error {0}'.format(str(e)))
        message += "Field Error. If you are using the report builder then you found a bug!"
        message += "If you made this in admin, then you probably did something wrong."
        values_and_properties_list = None

    return values_and_properties_list, message