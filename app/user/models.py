import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _

from common.kgs import generate_unique_id
from common.models import AuditableModel

from .enums import TOKEN_TYPE, USER_ROLE_CHOICES
from .managers import CustomUserManager, TokenManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, primary_key=True, default=generate_unique_id, editable=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    password = models.CharField(max_length=600, null=True)
    transfer_pin = models.CharField(max_length=400, null=True)
    admin_transaction_pin = models.CharField(max_length=400, null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=17, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email_verified_at = models.DateTimeField(null=True)
    phone_verified_at = models.DateTimeField(null=True)
    image = models.FileField(upload_to='user_images/', blank=True, null=True)
    region = models.ForeignKey('business.Region', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='users')
    state = models.ForeignKey('business.State', on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='users')
    lga = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=100, choices=USER_ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    regional_head = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='regional_reports')
    divisional_head = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='divisional_reports')

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


class Token(models.Model):
    objects = TokenManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    token_type = models.CharField(
        max_length=100, choices=TOKEN_TYPE, default='CreateToken')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True
