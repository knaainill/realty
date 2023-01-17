import random
import string

from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('Логин заполнен неверно'))
        user = self.model(email=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser должен иметь is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(
        verbose_name=_('Логин'),
        unique=True,
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=25,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=25,
        null=True,
        blank=True,
    )
    info = models.CharField(
        _('Информация'),
        max_length=2500,
        null=True,
        blank=True,
    )
    phone_number2 = PhoneNumberField(
        verbose_name=_('Второй номер телефона'),
        null=True,
        blank=True,
    )
    instagram_link = models.URLField(
        verbose_name=_('Ссылка на инстаграм'),
        null=True,
        blank=True,
    )
    lalafo_link = models.URLField(
        verbose_name=_('Ссылка на лалафо'),
        null=True,
        blank=True,
    )
    whatsapp_link = models.URLField(
        verbose_name=_('Ссылка на вотсапп'),
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        ordering = ('-is_active',)

    def __str__(self):
        return str(self.first_name)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class PasswordResetCode(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='password_reset_code', unique=True)
    code = models.CharField(max_length=6, unique=True)

    @staticmethod
    def activation_code_generator():
        while True:
            code = ''.join(random.choice(string.digits) for x in range(6))
            if not PasswordResetCode.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f'{self.user.phone_number}: {self.code}'


class RegisterResetCode(models.Model):
    phone_number = PhoneNumberField(unique=True)
    code = models.CharField(max_length=6, unique=True)

    @staticmethod
    def activation_code_generator():
        while True:
            code = ''.join(random.choice(string.digits) for x in range(6))
            if not RegisterResetCode.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f'{self.phone_number}: {self.code}'