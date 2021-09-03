from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# User manager
from api.utils import get_random_alphanumeric_string


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, name, role, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          name=name, role=role, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, name, role, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                "Superuser must be assigned to is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")
        return self.create_user(email, user_name, name, role, password, **other_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR'
        SUPERVISOR = 'SUPERVISOR'
        STOREKEEPER = 'STOREKEEPER'

    id = models.CharField(primary_key=True, unique=True,
                          editable=False, blank=True, max_length=30)
    user_name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(_('Email address'), unique=True)
    name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=Role.choices, default="")
    addDate = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name', 'role']

    objects = CustomAccountManager()

    def save(self, *args, **kwargs):
        while not self.id:
            newId = get_random_alphanumeric_string(20)

            if not User.objects.filter(pk=newId).exists():
                self.id = newId
        super(User, self).save()

    def __str__(self):
        return self.user_name
