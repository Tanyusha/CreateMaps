from django.core import validators

__author__ = 'pahaz'

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin, AbstractUser, UserManager
)


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_active=True,
                          is_superuser=is_superuser, )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                  'This value may contain only letters, numbers '
                  'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = True

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return "{0} ({1})".format(self.username, self.email.split('@')[0])

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'
