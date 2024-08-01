from typing import Any, Optional, TypeVar

from django.contrib.auth.models import AbstractBaseUser  # User를 상속 받도록 한다
from django.contrib.auth.models import PermissionsMixin  # super user, 일반 user를 구분하기 위해
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from common.models import Allergy, CommonModel

T = TypeVar("T", bound="User")


class UserManager(BaseUserManager[T]):
    # 일반 유저 생성 함수
    def create_user(self, username: str, email: str, password: Optional[str] = None, **extra_fields: Any) -> T:

        if not email:
            raise ValueError("Please enter your email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # 슈퍼 유저 생성 함수
    def create_superuser(self, username: str, email: str, password: Optional[str] = None, **extra_fields: Any) -> T:

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise TypeError("Superusers must have a password.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CommonModel):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=15, unique=True)
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    STORE = 2
    USER = 1

    STATUS_CHOICES = (
        (STORE, "store"),
        (USER, "user"),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=USER)

    # PermissionMixin: 권한 관리
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    allergies = models.ManyToManyField(Allergy, blank=True, related_name="users")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:  # 핵심 데이터를 볼 수 있게 설정
        return f"email: {self.email}, username: {self.username}"
