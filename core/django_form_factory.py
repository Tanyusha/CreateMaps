from core.database import DatabaseInitInfoType
from django import forms
from django.forms import TextInput


class HiddenField(forms.CharField):
    widget = forms.HiddenInput


class PasswordInput(TextInput):
    input_type = 'password'


class PasswordField(forms.CharField):
    widget = PasswordInput


DJANGO_FIELD_MAP = {
    DatabaseInitInfoType.STR: forms.CharField,
    DatabaseInitInfoType.INT: forms.IntegerField,
    DatabaseInitInfoType.FLOAT: forms.FloatField,
    DatabaseInitInfoType.FILEPATH: HiddenField,
    DatabaseInitInfoType.PASSWORD: PasswordField,
}


def make_form(fields):
    fields = {k: DJANGO_FIELD_MAP.get(v)() for k, v in fields}
    return type('Form', (forms.Form, ), fields)
