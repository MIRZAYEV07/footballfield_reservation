
from django.contrib.auth.base_user import BaseUserManager

from common.managers import BaseManager


class UserManager(BaseUserManager, BaseManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_field_owner", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_moderator(self, username, password, **extra_fields):
        extra_fields.setdefault("is_field_owner", True)

        if extra_fields.get("is_field_owner") is not True:
            raise ValueError("Moderator must have is_field_owner=True.")

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_field_owner", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_field_owner") is not True:
            raise ValueError("Superuser must have is_field_owner=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def get_or_create(self, username, password, **kwargs):
        try:
            instance = self.model.objects.get(username=username)
            return instance, False
        except self.model.DoesNotExist:
            instance = self.model.objects.create_user(
                username=username, password=password, **kwargs
            )
            return instance, True
