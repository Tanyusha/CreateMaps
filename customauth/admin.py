from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from customauth.forms import UserChangeForm, UserCreationForm
from customauth.models import MyUser

__author__ = 'pahaz'


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser', )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', )
    # filter_horizontal = ('groups', 'user_permissions',)


# Now register the new UserAdmin...
admin.site.register(MyUser, MyUserAdmin, )
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
