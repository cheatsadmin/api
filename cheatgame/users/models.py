from enum import IntEnum

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from cheatgame.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin


class VerifyType(IntEnum):
    PHONENUMBER = 1
    EMAIL = 2
    PASSWORD = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserTypes(IntEnum):
    CUSTOMER = 1
    ADMIN = 2
    MANAGER = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BaseUserManager(BUM):
    def create_user(self, phone_number, firstname, lastname, is_active=True, is_admin=False, password=None,
                    user_type=UserTypes.CUSTOMER):
        if not phone_number:
            raise ValueError("Users must have an phone_number")
        if not firstname:
            raise ValueError("users must have firstname")

        if not lastname:
            raise ValueError("Users must have lastname")

        user = self.model(phone_number=phone_number, firstname=firstname, lastname=lastname,
                          is_active=is_active, is_admin=is_admin, user_type=user_type)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, firstname='test', lastname='test', password=None,
                         user_type=UserTypes.MANAGER):
        user = self.create_user(
            phone_number=phone_number,
            firstname=firstname,
            lastname=lastname,
            is_active=True,
            is_admin=True,
            password=password,
            user_type=user_type,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    user_type = models.IntegerField(choices=UserTypes.choices(), default=UserTypes.CUSTOMER)
    firstname = models.CharField(verbose_name='first_name',
                                 max_length=100)
    lastname = models.CharField(verbose_name="last_name",
                                max_length=100)
    phone_number = models.CharField(verbose_name="phone_number",
                                    unique=True, max_length=11)
    email = models.EmailField(verbose_name="email address",
                              unique=True, null=True, blank=True)
    profile_image = models.FileField(null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    birthdate = models.DateField(null=True, blank=True)
    verify_type = models.IntegerField(choices=VerifyType.choices(), null=True, blank=True)
    secret_key = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f'{self.firstname}-{self.lastname}'

    def is_staff(self):
        return self.is_admin


class Address(BaseModel):
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=15)
    address_detail = models.TextField(max_length=400)
    user = models.ForeignKey("BaseUser", on_delete=models.CASCADE, related_name="addresses")

    def __str__(self):
        return f"{self.postal_code}-{self.user.lastname}"


class FavoriteProduct(BaseModel):
    user = models.ForeignKey("BaseUser", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.lastname}-{self.product.title}"
