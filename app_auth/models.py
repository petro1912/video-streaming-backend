# pylint: disable=missing-docstring
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccoutManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError("User must have an email.")
        
        user = self.model(
            email = email,
            fullname = fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(verbose_name='date_joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = MyAccoutManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
