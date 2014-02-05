#Monkey patch on django rest framework for supporting nulls:
# https://github.com/tomchristie/django-rest-framework/issues/384
from rest_framework import serializers


class NullSerializerPatch(serializers.BaseSerializer):

    def field_to_native(self, obj, field_name):

        if obj is None:
            return None
        val = getattr(obj, self.source or field_name, None)

        if self.source:
            val = obj
            for component in self.source.split('.'):
                val = getattr(val, component, None)

        if val is None:
            return None

        return super(NullSerializerPatch, self).field_to_native(obj, field_name)


class GetInfoManyRelatedField(serializers.ManyRelatedField):
    """
    Gets information from a model's (get_info method). Used to
    customize the serializers ManyRelatedField. Otherwise we only
    get a __unicode__ response. Must define get_info method on
    the model to use it.

    """
    def to_native(self, obj):
        if obj:
            return obj.get_info()
        else:
            return None


class GetInfoRelatedField(serializers.RelatedField):
    def to_native(self, obj):
        if obj:
            return obj.get_info()
        else:
            return None


class CleanRelatedField(serializers.Field):
    def field_to_native(self, obj, field_name):
        if obj is None:
            return '---'
        val = getattr(obj, self.source or field_name, None)

        if self.source:
            val = obj
            for component in self.source.split('.'):
                val = getattr(val, component, None)
        if val is None:
            return '---'

        return super(CleanRelatedField,self).field_to_native(obj, field_name)