__author__ = 'jbennett'
from django.contrib import admin
from cascade.libs.admin import SiteAdmin
from models import CartServiceType, CartStatus, CartType, TicketStatus,\
    AdminDefaults, ZipCodes, ServiceReasonCodes, Route, CollectionAddress, Cart, Ticket, CollectionCustomer,\
    CartServiceCharge, CartParts, InventoryAddress, DataErrors


class CartServiceChargeAdmin(admin.ModelAdmin):
    search_fields = ['amount', 'description']


class DataErrorsAdmin(admin.ModelAdmin):
    search_fields = ['error_type', 'failed_data']
    list_display = ['id', 'error_type', 'failed_data']
    list_filter = ['error_type', 'failed_data']



class CollectionCustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['__str__', 'site']

class CollectionAddressAdmin(admin.ModelAdmin):
    search_fields = ['house_number', 'street_name']
    list_filter = ['route__route_day', 'route__route_type', 'route__route', 'city']
    list_display = ['__str__', 'site']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['serial_number', 'rfid', 'location__street_name', 'location__house_number']
    list_filter = ['current_status__label', 'cart_type__name', 'cart_type__size', 'born_date', 'site']
    list_display = ['__str__', 'site']


class ZipcodesAdmin(admin.ModelAdmin):
    list_display = ['zipcode', 'site']
    list_filter = ['site']

class AdminDefaultsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'site', 'zipcodes']

    def zipcodes(self, obj):
        z = []
        for zipcodes in obj.default_zipcodes.all():
             z.append(str(zipcodes.zipcode))
        return z


class CartPartsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'on_hand']



class TicketAdmin(admin.ModelAdmin):
    search_fields = ['serviced_cart__serial_number', 'serviced_cart__rfid',
                     'expected_cart__serial_number', 'expected_cart__rfid',
                     'location__street_name', 'location__house_number']
    list_filter = ['service_type__code', 'status__service_status', 'created_online']
    list_display = ['__str__', 'site', 'created_online']

admin.site.register(DataErrors, DataErrorsAdmin)
admin.site.register(InventoryAddress)
admin.site.register(CartServiceType)
admin.site.register(CartStatus)
admin.site.register(CartType)
admin.site.register(CartParts, CartPartsAdmin)
admin.site.register(TicketStatus)
admin.site.register(AdminDefaults, AdminDefaultsAdmin)
admin.site.register(ZipCodes, ZipcodesAdmin)
admin.site.register(ServiceReasonCodes)
admin.site.register(Route)
admin.site.register(CollectionAddress, CollectionAddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CollectionCustomer, CollectionCustomerAdmin)
admin.site.register(CartServiceCharge, CartServiceChargeAdmin)