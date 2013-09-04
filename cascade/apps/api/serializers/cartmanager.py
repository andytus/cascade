from rest_framework import serializers
from cascade.apps.cartmanager.models import Cart, CollectionAddress, CollectionCustomer, CartStatus, CartType, \
    Ticket, AdminDefaults, CartsUploadFile, TicketsCompleteUploadFile, CustomersUploadFile, TicketStatus,\
    TicketComments, CartServiceType

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


class CartLocationCustomerField(serializers.Field):
    def to_native(self, value):
        if value == None or value.customer == None:
            return "Not Assigned"
        else:
            return value.customer.get_info()

class CustomerInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')

    class Meta:
        model = CollectionCustomer
        fields = ('info',)

class LocationInfoSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_info')
    class Meta:
        model = CollectionAddress
        exclude = ('site',)
        fields = ('info',)
        ############################################

class CartStatusSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CartStatus
        exclude = ('site',)

class CartTypeSerializer(serializers.ModelSerializer, NullSerializerPatch):

    class Meta:
        model = CartType
        depth = 1
        exclude = ('site',)

class AddressCartProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    customer = CustomerInfoSerializer()
    class Meta:
        model = CollectionAddress
        depth = 1
        exclude = ('site',)


class CartProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = AddressCartProfileSerializer()
    current_status = CartStatusSerializer()
    cart_type = CartTypeSerializer()
    cart_url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = Cart
        depth = 1
        exclude = ('updated_by', 'inventory_location', 'file_upload')


class CartSearchSerializer(serializers.ModelSerializer, NullSerializerPatch):
    location = GetInfoRelatedField(source='location')
    inventory_location = GetInfoRelatedField(source='inventory_location')
    customer = CartLocationCustomerField(source='location')
    cart = serializers.Field(source='get_info')

    class Meta:
        model = Cart
        fields = ('cart', 'customer', 'location', 'inventory_location')


class CartServiceTicketSerializer(serializers.ModelSerializer, NullSerializerPatch):

    serviced_cart__serial_number = CleanRelatedField(source='serviced_cart.serial_number')
    serviced_cart__id = CleanRelatedField(source='serviced_cart.id')
    serviced_cart__cart_type__name = CleanRelatedField(source='serviced_cart.cart_type.name')
    serviced_cart__cart_type__size = CleanRelatedField(source='serviced_cart.cart_type.size')
    expected_cart__serial_number = CleanRelatedField(source='expected_cart.serial_number')
    expected_cart__id = CleanRelatedField(source='expected_cart.id')

    status__service_status = CleanRelatedField(source='status.service_status')
    status__level = CleanRelatedField(source='status.level')
    service_type__code = CleanRelatedField(source='service_type.code')
    service_type__service = CleanRelatedField(source='service_type.service')

    #Cart Requested Info####################################
    cart_type__name = CleanRelatedField(source='cart_type.name')
    cart_type__size = CleanRelatedField(source='cart_type.size')
    ########################################################

    #Location Info###############################################
    location__house_number = CleanRelatedField(source='location.house_number')
    location__street_name = CleanRelatedField(source='location.street_name')
    location__unit = serializers.RelatedField(source='location.unit')
    location__customer__get_absolute_url = CleanRelatedField(source='location.customer.get_absolute_url')
    location__customer__get_app_url = CleanRelatedField(source='location.customer.get_app_url')
    #############################################################

    created_by__username = CleanRelatedField(source='created_by.username')
    updated_by__username = CleanRelatedField(source='updated_by.username')

    class Meta:
        model = Ticket
        fields = ('id', 'service_type__code', 'service_type__service', 'success_attempts',
                  'serviced_cart__serial_number', 'serviced_cart__id', 'serviced_cart__cart_type__size',
                  'serviced_cart__cart_type__name', 'expected_cart__serial_number', 'status__service_status', 'status__level', 'processed',
                  'date_completed', 'date_created', 'date_processed', 'date_last_attempted',
                  'longitude', 'latitude', 'device_name', 'audit_status', 'location__house_number', 'location__street_name', 'location__unit',
                  'location__customer__get_absolute_url', 'location__customer__get_app_url', 'cart_type__name',
                  'cart_type__size', 'created_by__username', 'updated_by__username')


class TicketCommentSerializer(serializers.ModelSerializer, NullSerializerPatch):
    created_by = CleanRelatedField(source='created_by.username')
    class Meta:
        model = TicketComments
        exclude = ('site', )



class TicketStatusSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = TicketStatus
        exclude = ('site',)

class CartServiceTypeSerializer(serializers.ModelSerializer, NullSerializerPatch):
    class Meta:
        model = CartServiceType
        exclude = ("site", )


class CustomerProfileSerializer(serializers.ModelSerializer, NullSerializerPatch):

    class Meta:
        model = CollectionCustomer
        depth = 1
        exclude = ('site',)


class AdminLocationDefaultSerializer(serializers.ModelSerializer, NullSerializerPatch):
    info = serializers.Field('get_location_info')
    class Meta:
        model = AdminDefaults
        depth = 1
        fields = ('info',)


class UploadFileSerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    file_kind = serializers.CharField()
    status = serializers.CharField()
    num_good = serializers.IntegerField()
    num_error = serializers.IntegerField()
    num_records = serializers.IntegerField()
    uploaded_by = serializers.CharField()
    date_uploaded = serializers.DateTimeField()
    date_start_processing = serializers.DateTimeField()
    size = serializers.IntegerField()
    message = serializers.CharField()