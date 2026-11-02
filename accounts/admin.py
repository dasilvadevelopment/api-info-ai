from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserAccount


class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False
    fk_name = 'user'


class UserWithDepartmentAdmin(UserAdmin):
    inlines = [UserAccountInline]


admin.site.unregister(User)
admin.site.register(User, UserWithDepartmentAdmin)

