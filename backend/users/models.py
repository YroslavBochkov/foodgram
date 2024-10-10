import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


ROLES = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
]

ACCESS_LEVEL = {
    'user': 1,
    'admin': 2,
}


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с аватаром."""

    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')]
    )
    email = models.EmailField('Email пользователя', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField('Роль пользователя', max_length=15, choices=ROLES, default='user')
    confirmation_code = models.UUIDField('Код подтверждения', default=uuid.uuid4)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def has_access(self):
        return self._access

    @has_access.setter
    def has_access(self, role):
        """Проверяет уровень доступа пользователя."""
        self._access = (
            ACCESS_LEVEL[self.role] <= ACCESS_LEVEL[role]
            or self.is_superuser
        )

    def __str__(self):
        return self.username
