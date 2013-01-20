__author__ = 'jbennett'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from cascade.apps.cartmanager.models import UserAccountProfile


class UserAccountProfileInline(admin.StackedInline):
    model = UserAccountProfile
    filter_horizontal = ('sites',)
    can_delete = False
    verbose_name = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserAccountProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
