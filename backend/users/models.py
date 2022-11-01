from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Переопределенный пользователь """
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Subscribe(models.Model):
    """ Подписка на пользователя """
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
