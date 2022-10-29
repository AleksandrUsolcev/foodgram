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


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscribed'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписан на',
        related_name='subscribers'
    )
    date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_sub',
            )
        ]

    def __str__(self):
        return f'{self.user} sub to {self.author}'
