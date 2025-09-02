import uuid
from django.core.cache import cache
from enum import StrEnum, auto
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .tasks import send_activation_email

class Role (StrEnum):
    ADMIN = auto()
    SUPPORT = auto()
    DRIVER = auto()
    CUSTOMER = auto()

    @classmethod
    def choices(cls):
        results = []

        for item in cls:
            _element = item.value, item.name.lower().capitalize()
            results.append(_element)
        return results

class UserManager(BaseUserManager):
    use_in_migration = True
    def create_user(self, email , password=None, **extra_fields):
        email = self.normalize_email(email)


        #extra_fields["is_staff"] = False
        #extra_fields["is_superuser"] = False
        #extra_fields["role"] = Role.CUSTOMER

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email , password=None, **extra_fields):
        #email = self.normalize_email(email)
        #password = make_password(password)

        extra_fields["is_staff"] = True
        extra_fields["is_active"] = True
        extra_fields["is_superuser"] = True
        extra_fields["role"] = Role.ADMIN
        return self.create_user(email, password,**extra_fields)

        #user = self.model(email=email, password=password, **extra_fields)

        #user.save()

        #return user


class User (AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "users"
    objects = UserManager()

    email = models.EmailField(max_length=100, unique=True, null=False)
    phone_number = models.CharField (max_length=10, unique=True, null= True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=50, null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    activation_code = models.UUIDField(default=uuid.uuid4,  null=True, blank=True)


    role = models.CharField(max_length=50, default=Role.CUSTOMER, choices=Role.choices())
    date_joined = models.DateTimeField(default=timezone.now)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def send_activation_code(self):
     #   code = str(uuid.uuid4())
     #   cache.set(code, self.email, timeout=600)


      #  activation_link = f"{settings.SITE_URL}/activate/{code}/"
      #  subject = "Activate your account"
      #  message = f"Hi {self.first_name}, please click the link to activate your account: {activation_link}"

     #  send_mail(
      #      subject,
      #      message,
     #       settings.DEFAULT_FROM_EMAIL,
      #      [self.email],
      #      fail_silently=False,
      #  )
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save(update_fields=["activation_code"])
        cache.set(code, self.email, timeout=600)
        activation_link = f"{settings.SITE_URL}/activate/{code}/"
        send_activation_email(self.email, self.first_name, activation_link)