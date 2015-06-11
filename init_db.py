from django.core import serializers
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")
django.setup()
from django.conf import settings
from customauth.models import MyUser
from django.contrib.auth.models import Group


AUTH = """
[
    {
        "fields": {
            "codename": "add_logentry",
            "name": "Can add log entry",
            "content_type": 1
        },
        "pk": 1,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_logentry",
            "name": "Can change log entry",
            "content_type": 1
        },
        "pk": 2,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_logentry",
            "name": "Can delete log entry",
            "content_type": 1
        },
        "pk": 3,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_permission",
            "name": "Can add permission",
            "content_type": 2
        },
        "pk": 4,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_permission",
            "name": "Can change permission",
            "content_type": 2
        },
        "pk": 5,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_permission",
            "name": "Can delete permission",
            "content_type": 2
        },
        "pk": 6,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_group",
            "name": "Can add group",
            "content_type": 3
        },
        "pk": 7,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_group",
            "name": "Can change group",
            "content_type": 3
        },
        "pk": 8,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_group",
            "name": "Can delete group",
            "content_type": 3
        },
        "pk": 9,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_contenttype",
            "name": "Can add content type",
            "content_type": 4
        },
        "pk": 10,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_contenttype",
            "name": "Can change content type",
            "content_type": 4
        },
        "pk": 11,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_contenttype",
            "name": "Can delete content type",
            "content_type": 4
        },
        "pk": 12,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_session",
            "name": "Can add session",
            "content_type": 5
        },
        "pk": 13,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_session",
            "name": "Can change session",
            "content_type": 5
        },
        "pk": 14,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_session",
            "name": "Can delete session",
            "content_type": 5
        },
        "pk": 15,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_map",
            "name": "Can add \u043a\u0430\u0440\u0442\u0430",
            "content_type": 6
        },
        "pk": 16,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_map",
            "name": "Can change \u043a\u0430\u0440\u0442\u0430",
            "content_type": 6
        },
        "pk": 17,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_map",
            "name": "Can delete \u043a\u0430\u0440\u0442\u0430",
            "content_type": 6
        },
        "pk": 18,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_dataset",
            "name": "Can add dataset",
            "content_type": 7
        },
        "pk": 19,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_dataset",
            "name": "Can change dataset",
            "content_type": 7
        },
        "pk": 20,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_dataset",
            "name": "Can delete dataset",
            "content_type": 7
        },
        "pk": 21,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_mobject",
            "name": "Can add m object",
            "content_type": 8
        },
        "pk": 22,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_mobject",
            "name": "Can change m object",
            "content_type": 8
        },
        "pk": 23,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_mobject",
            "name": "Can delete m object",
            "content_type": 8
        },
        "pk": 24,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_point",
            "name": "Can add point",
            "content_type": 9
        },
        "pk": 25,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_point",
            "name": "Can change point",
            "content_type": 9
        },
        "pk": 26,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_point",
            "name": "Can delete point",
            "content_type": 9
        },
        "pk": 27,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_field",
            "name": "Can add field",
            "content_type": 10
        },
        "pk": 28,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_field",
            "name": "Can change field",
            "content_type": 10
        },
        "pk": 29,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_field",
            "name": "Can delete field",
            "content_type": 10
        },
        "pk": 30,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "add_myuser",
            "name": "Can add \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c",
            "content_type": 11
        },
        "pk": 31,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "change_myuser",
            "name": "Can change \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c",
            "content_type": 11
        },
        "pk": 32,
        "model": "auth.permission"
    },
    {
        "fields": {
            "codename": "delete_myuser",
            "name": "Can delete \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c",
            "content_type": 11
        },
        "pk": 33,
        "model": "auth.permission"
    },
    {
        "fields": {
            "permissions": [
                19,
                20,
                21,
                28,
                29,
                30,
                16,
                17,
                18,
                22,
                23,
                24,
                25,
                26,
                27
            ],
            "name": "user"
        },
        "pk": 1,
        "model": "auth.group"
    }
]
"""

for obj in serializers.deserialize('json', AUTH):
    obj.save()

try:
    user = MyUser.objects.get(username='admin')
except MyUser.DoesNotExist:
    user = MyUser.objects.create(username='admin', email='admin@test.com')

user.set_password('qwer')
user.is_superuser = True
user.save()

try:
    user = MyUser.objects.get(username='user')
except MyUser.DoesNotExist:
    user = MyUser.objects.create(username='user', email='user@test.com')

user.set_password('qwer')
user.save()

user.groups.add(Group.objects.get(name='user'))
