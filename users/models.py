from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def craete_user(self, email, password):
        if not email:
            raise ValueError("올바른 이메일을 입력하세요.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.craete_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)


# 암호화는 qwer1234 -> asdasdqweq2131 -> 복호화 -> qwer1234
# 해쉬화는 qwer1234 -> asdase / dqwe2123 -> 암호화(asdase) -> 암호화 반복 -> qweqweqr -> 복호화가 불가능
# django는 SHA256을 사용


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField("nickname", max_length=20, unique=True)
    phone = models.CharField("phone", max_length=20, unique=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "유저"
        verbose_name_plural = f"{verbose_name} 목록"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

# user.is_super() -> user.is_super 로 바꿔줌


