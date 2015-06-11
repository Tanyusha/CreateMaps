# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import customauth.models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True,
                                        verbose_name='ID', auto_created=True)),
                ('password',
                 models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                                                    verbose_name='last login')),
                ('is_superuser',
                 models.BooleanField(verbose_name='superuser status',
                                     default=False,
                                     help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username',
                 models.CharField(
                     max_length=30, verbose_name='username',
                     validators=[
                         django.core.validators.RegexValidator(
                             '^[\\w.@+-]+$',
                             'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.',
                             'invalid')], unique=True,
                     error_messages={
                         'unique': 'A user with that username already exists.'},
                     help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('email', models.EmailField(max_length=255, unique=True,
                                            verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('groups',
                 models.ManyToManyField(blank=True, verbose_name='groups',
                                        related_query_name='user',
                                        to='auth.Group',
                                        related_name='user_set',
                                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(blank=True,
                                                            verbose_name='user permissions',
                                                            related_query_name='user',
                                                            to='auth.Permission',
                                                            related_name='user_set',
                                                            help_text='Specific permissions for this user.')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', customauth.models.MyUserManager()),
            ],
        ),
    ]
