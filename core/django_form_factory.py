from core.database import DatabaseInitInfoType
from django import forms


class HiddenField(forms.CharField):
    widget = forms.HiddenInput

DJANGO_FIELD_MAP = {
    DatabaseInitInfoType.STR: forms.CharField,
    DatabaseInitInfoType.INT: forms.IntegerField,
    DatabaseInitInfoType.FLOAT: forms.FloatField,
    DatabaseInitInfoType.FILEPATH: HiddenField,
}


def make_form(fields):
    fields = {k: DJANGO_FIELD_MAP.get(v)() for k, v in fields.items()}
    print(fields)
    return type('Form', (forms.Form, ), fields)
