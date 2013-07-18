__author__ = 'jbennett'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import CartServiceType, CartStatus, CartType, TicketStatus, AdminDefaults, ZipCodes, ServiceReasonCodes


from cascade.apps.cartmanager.models import UserAccountProfile, InventoryAddress


class UserAccountProfileInline(admin.StackedInline):
    model = UserAccountProfile
    filter_horizontal = ('sites',)
    can_delete = False
    verbose_name = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserAccountProfileInline,)





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