from django.forms import widgets
from rest_framework import serializers
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


class CustomerInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')

    class Meta:
        model = CollectionCustomer
        fields = ('info',)

class AddressInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')
    class Meta:
        model = CollectionAddress
        fields = ('info',)


class CollectionAddressSerializer(serializers.ModelSerializer, NullSerializerPatch):
    customer = CustomerInfoSerializer()
    class Meta:
        model = CollectionAddress

class CartDetailsSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = CollectionAddressSerializer()
    class Meta:
        model = Cart
        depth = 1


class CustomerInfoSearch(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CollectionCustomer

class CartSearchSerializer(serializers.ModelSerializer, NullSerializerPatch):

    class Meta:
        model = Cart

class LocationSearchSerializer(serializers.ModelSerializer, NullSerializerPatch):
    pass

#    location = serializers.Field(source='get_info')
#    customer = GetInfoRelatedField(source='customer')
#    carts = GetInfoManyRelatedField(source='location') #serializers.ManyRelatedField(source='location').to_native("test")
#
#    class Meta:
#        model = CollectionAddress
#        fields = ('location', 'carts', 'customer')


class LocationCustomer(serializers.ModelSerializer):
    customer = GetInfoRelatedField(source='customer')
    class Meta:
        model = CollectionAddress
        field = ('customer', 'id')

class CartLocationCustomerField(serializers.Field):
    def to_native(self, value):
        if value.customer == None:
            print value.customer
            return "Not Assigned"
        else:
            return value.customer.get_info()

class CartLocationSearchSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = GetInfoRelatedField(source='location')
    customer = CartLocationCustomerField(source='location')
    cart = serializers.Field(source='get_info')

    class Meta:
        model = Cart
        fields = ('cart', 'customer', 'location')


