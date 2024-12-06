import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from pykolofinance.common.kgs import generate_unique_id
from pykolofinance.common.models import AuditableModel

from .enums import TOKEN_TYPE, USER_ROLE_OPTIONS
from .managers import CustomUserManager, TokenManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, primary_key=True, default=generate_unique_id, editable=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    phone = models.CharField(max_length=17, unique=True)
    password = models.CharField(max_length=600, null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLE_OPTIONS, default='Merchant')
    email_verified_at = models.DateTimeField(null=True)
    phone_verified_at = models.DateTimeField(null=True)
    image = models.FileField(upload_to='user_images/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('lastname', 'firstname')

    def __str__(self):
        return self.email

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    def save_last_login(self):
        self.last_login = make_aware(datetime.now())
        self.save()

    def verify_user(self):
        self.verified = True
        self.save()


class Token(AuditableModel):
    objects = TokenManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    token_type = models.CharField( max_length=100, choices=TOKEN_TYPE, default='CreateToken')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = make_aware(datetime.now())
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True
