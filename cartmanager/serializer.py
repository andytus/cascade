from django.forms import widgets
from rest_framework import serializers, pagination
from models import Cart, CollectionAddress, CollectionCustomer

#Monkey patch on django rest framework for supporting nulls: https://github.com/tomchristie/django-rest-framework/issues/384
class NullSerializerPatch(serializers.BaseSerializer):
    def field_to_native(self, obj, field_name):
        if obj is None:
            return None
        val = getattr(obj, self.source or field_name)
        if val is None:
            return None
        return super(NullSerializerPatch,self).field_to_native(obj, field_name)

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

class CartLocationCustomerField(serializers.Field):
    def to_native(self, value):
        if value.customer == None:
            return "Not Assigned"
        else:
            return value.customer.get_info()

class CustomerInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')

    class Meta:
        model = CollectionCustomer
        fields = ('info',)

class CustomerProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CollectionCustomer
        depth = 1

class AddressInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')
    class Meta:
        model = CollectionAddress
        fields = ('info',)

class AddressProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    customer = CustomerInfoSerializer()
    class Meta:
        model = CollectionAddress
        depth = 1

class CartProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = AddressProfileSerializer()
    class Meta:
        model = Cart
        depth = 1

class CartSearchSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = GetInfoRelatedField(source='location')
    customer = CartLocationCustomerField(source='location')
    cart = serializers.Field(source='get_info')

    class Meta:
        model = Cart
        fields = ('cart', 'customer', 'location')

class CartLocationUpdateSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = Cart
        fields = ('location',)