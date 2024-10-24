from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from users.validators import validate_username_not_me

from foodgram import constants


class CustomUser(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    email = models.EmailField(
        max_length=constants.EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        verbose_name="Адрес электронной почты",
        error_messages={
            "unique": "Пользователь с таким адресом уже зарегистрирован",
        },
    )
    username = models.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username_not_me],
        verbose_name="Имя пользователя",
        error_messages={
            "unique": "Пользователь уже существует",
        },
    )
    first_name = models.CharField(
        max_length=constants.FIRSTNAME_MAX_LENGTH, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=constants.LASTNAME_MAX_LENGTH, verbose_name="Фамилия"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="Аватар",
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribed_to",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(name='unique_subscription',
                                    fields=["user", "author"])
        ]

    def __str__(self):
        return f"{self.user.username} вы подписаны на {self.author.username}"
