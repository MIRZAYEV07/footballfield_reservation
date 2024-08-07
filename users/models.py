
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from users.managers import UserManager
from users.utils import user_expire_time


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    expiration_time_register = models.CharField(max_length=100,null=True, blank=True, default=user_expire_time)
    expiration_time_reset = models.CharField(max_length=100,null=True, blank=True)
    is_field_owner = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        ordering = ("-id",)
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def get_full_name(self):

        return f"{self.first_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.username} {self.first_name}"