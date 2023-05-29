import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from core.models import TimestampedModel
from core.utils.typing import Empty

# Create your models here.


class AuthSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    email_code = models.CharField(max_length=12)
    exp = models.CharField(max_length=12)
    at = models.CharField(max_length=12)
    attempt = models.IntegerField(default=1)

    class Meta:
        db_table = 'users_auth_session'

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def update(self, **kwargs):
        update_fields = []
        for key, value in kwargs.items():
            if not isinstance(value, Empty):
                setattr(self, key, value)
                update_fields.append(key)
        self.save(update_fields=update_fields)


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None) -> 'User':
        if username is None:
            raise TypeError('Users must have a username.')
        
        user = self.model(username=username, email=self.normalize_email(email) if email is not None else email)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email=None, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def update(self, **kwargs):
        update_fields = []
        for key, value in kwargs.items():
            if not isinstance(value, Empty):
                setattr(self, key, value)
                update_fields.append(key)
        self.save(update_fields=update_fields)
