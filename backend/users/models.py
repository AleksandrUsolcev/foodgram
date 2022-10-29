from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Переопределенный пользователь """
    ADMIN = 'admin'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (USER, 'Авторизованный пользователь')
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        max_length=10,
        default='user'
    )

    @property
    def role_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
