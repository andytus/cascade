from rest_framework import serializers
from cascade.apps.cartmanager.models import Cart, CollectionAddress, CollectionCustomer, CartStatus, CartType, \
    CartServiceTicket

#Monkey patch on django rest framework for supporting nulls: https://github.com/tomchristie/django-rest-framework/issues/384
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
        exclude = ('site',)

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
        exclude = ('site',)

class CartStatusSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CartStatus
        depth = 1
        exclude = ('site',)

class CartTypeSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CartType
        depth = 1
        exclude = ('site',)


class CartProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = AddressProfileSerializer()
    current_status = CartStatusSerializer()
    cart_type = CartTypeSerializer()
    class Meta:
        model = Cart
        depth = 1
        exclude = ('site',)

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


class CartServiceTicketSerializer(serializers.ModelSerializer, NullSerializerPatch):
    #TODO do a get_info on CartServiceTicket (with info from removed cart ...size, etc)

    removed_cart = CleanRelatedField(source='removed_cart.rfid')
    removed_cart_size = CleanRelatedField(source='removed_cart.cart_type.size')
    audit_cart = CleanRelatedField(source='audit_cart.rfid')

    #Assigned after complete######################################
    delivered_cart = CleanRelatedField(source='delivered_cart.rfid')

    status = CleanRelatedField(source='status.service_status')
    service_type = CleanRelatedField(source='service_type.code')

    #Cart Requested Info####################################
    cart_type = CleanRelatedField(source='cart_type.name')
    cart_type_size = CleanRelatedField(source='cart_type.size')
    ########################################################

    #Location Info###############################################
    house_number =CleanRelatedField(source='location.house_number')
    street_name = CleanRelatedField(source='location.street_name')
    unit = CleanRelatedField(source='location.unit')
    #############################################################

    class Meta:
        model = CartServiceTicket
        fields = ( 'id','service_type', 'success_attempts', 'audit_cart', 'removed_cart', 'removed_cart_size',
                  'delivered_cart', 'status', 'date_completed', 'date_created', 'date_last_accessed', 'latitude',
                  'longitude', 'device_name', 'audit_status', 'broken_component', 'broken_comments', 'house_number',
                   'street_name', 'unit', 'cart_type','cart_type_size')


