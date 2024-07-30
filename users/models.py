from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # User를 상속 받도록 한다
    PermissionsMixin,  # super user, 일반 user를 구분하기 위해
    BaseUserManager,
    AbstractUser,
)
from common.models import CommonModel, Allergy


class UserManager(BaseUserManager):
    # 일반 유저 생성 함수
    def create_user(self, username, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Please enter your email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # 슈퍼 유저 생성 함수
    def create_superuser(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise TypeError("Superusers must have a password.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CommonModel):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=15, unique=True)
    id = models.AutoField(primary_key=True)
    # PermissionMixin: 권한 관리
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    allergies = models.ManyToManyField(Allergy, blank=True, related_name="users")

    USERNAME_FIELD = "username"  # USERNAME_FIELD로 정의가 되어있는 필드는 unique=True가 필요
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]  # Required_fields를 설정하지 않으면 추가적인 필드를 강제할 수 있습니다.

    objects = UserManager()  # 유저를 생성 및 관리 (유저를 구분해서 관리하기 위해 - 관리자계정, 일반계정)

    def __str__(self):  # 핵심 데이터를 볼 수 있게 설정
        return f"email: {self.email}, username: {self.username}"
