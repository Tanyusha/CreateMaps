from core.admin import OwnableAdmin
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from maps.models import Map, Field

__author__ = 'pahaz'


class FieldInlineAdmin(admin.StackedInline):
    model = Field
    extra = 1


class MapAdmin(OwnableAdmin):
    search_fields = ('name', 'description',)
    filter_horizontal = ('editors',)
    inlines = (FieldInlineAdmin, )

    def save_form(self, request, form, change):
        """
        Set the object's owner as the logged in user.
        """
        map = super(MapAdmin, self).save_form(request, form, change)
        map.save()
        map.editors.add(map.user)
        return map

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        if request.user.is_superuser:
            return 'name', 'description', 'user'
        return 'name', 'description'

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (None, {'fields': ('user', 'name', 'description')}),
                (_('Permissions'), {'fields': ('editors',)}),
            )
        return (
            (None, {'fields': ('name', 'description')}),
            (_('Permissions'), {'fields': ('editors',)}),
        )

# Now register the new UserAdmin...
admin.site.register(Map, MapAdmin)
