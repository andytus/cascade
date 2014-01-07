__author__ = 'jbennett'

from django.contrib import admin
from models import CartServiceType, CartStatus, CartType, TicketStatus,\
    AdminDefaults, ZipCodes, ServiceReasonCodes, Route, CollectionAddress, Cart, Ticket, CollectionCustomer,\
    CartServiceCharge, CartParts, InventoryAddress

class CartServiceChargeAdmin(admin.ModelAdmin):
    search_fields = ['amount', 'description']

class CollectionCustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']


class CollectionAddressAdmin(admin.ModelAdmin):
    search_fields = ['house_number', 'street_name']
    list_filter = ['route__route_day', 'route__route_type', 'route__route', 'city']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['serial_number', 'rfid', 'location__street_name', 'location__house_number']
    list_filter = ['current_status__label', 'cart_type__name', 'cart_type__size', 'born_date']


class CartPartsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'on_hand']



class TicketAdmin(admin.ModelAdmin):
    search_fields = ['serviced_cart__serial_number', 'serviced_cart__rfid',
                     'expected_cart__serial_number', 'expected_cart__rfid',
                     'location__street_name', 'location__house_number']
    list_filter = ['service_type__code', 'status__service_status']


admin.site.register(InventoryAddress)
admin.site.register(CartServiceType)
admin.site.register(CartStatus)
admin.site.register(CartType)
admin.site.register(CartParts, CartPartsAdmin)
admin.site.register(TicketStatus)
admin.site.register(AdminDefaults)
admin.site.register(ZipCodes)
admin.site.register(ServiceReasonCodes)
admin.site.register(Route)
admin.site.register(CollectionAddress, CollectionAddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CollectionCustomer, CollectionCustomerAdmin)
admin.site.register(CartServiceCharge, CartServiceChargeAdmin)