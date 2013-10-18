__author__ = 'jbennett'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import CartServiceType, CartStatus, CartType, TicketStatus,\
    AdminDefaults, ZipCodes, ServiceReasonCodes, Route, CollectionAddress,Cart, Ticket


from cascade.apps.cartmanager.models import UserAccountProfile, InventoryAddress


class CollectionAddressAdmin(admin.ModelAdmin):
    search_fields = ['house_number', 'street_name']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['serial_number', 'rfid', 'location__street_name', 'location__house_number']
    list_filter = ['current_status__label', 'cart_type__name', 'cart_type__size', 'born_date']


class UserAccountProfileInline(admin.StackedInline):
    model = UserAccountProfile
    filter_horizontal = ('sites',)
    can_delete = False
    verbose_name = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserAccountProfileInline,)


class TicketAdmin(admin.ModelAdmin):
    search_fields = ['serviced_cart__serial_number', 'serviced_cart__rfid',
                     'expected_cart__serial_number', 'expected_cart__rfid',
                     'location__street_name', 'location__house_number']
    list_filter = ['service_type__code', 'status__service_status']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(InventoryAddress)
admin.site.register(CartServiceType)
admin.site.register(CartStatus)
admin.site.register(CartType)
admin.site.register(TicketStatus)
admin.site.register(AdminDefaults)
admin.site.register(ZipCodes)
admin.site.register(ServiceReasonCodes)
admin.site.register(Route)
admin.site.register(CollectionAddress, CollectionAddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Ticket, TicketAdmin)