from django.db import models

from users.models import User


class Tag(models.Model):
    """ Тег рецепта """
    name = models.CharField(
        verbose_name='Название',
        max_length=254
    )
    color = models.CharField(
        verbose_name='HEX-код',
        max_length=7
    )
    slug = models.SlugField(
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    """ Ингредиент """
    name = models.CharField(
        verbose_name='Название',
        max_length=254
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """ Рецепт """
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class ShoppingCart(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='В списке',
        related_name='users'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'ingredient'],
                name='unique_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} add to cart {self.ingredient}'


class Favorite(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='В избранном',
        related_name='users'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]

    def __str__(self):
        return f'{self.user} follow {self.recipe}'
