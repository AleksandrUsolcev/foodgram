from django.db import models

from users.models import User


class Tag(models.Model):
    """ Тег рецепта """

    CRIMSON = '#DC143C'
    PALE_VIOLET_RED = '#DB7093'
    ORANGE = '#FFA500'
    DARK_KHAKI = '#BDB76B'
    VIOLET = '#EE82EE'
    CHOCOLATE = '#D2691E'
    SILVER = '#C0C0C0'
    LIME = '#00FF00'
    DEEP_SKY_BLUE = '#00BFFF'
    OLIVE = '#808000'

    COLORS = (
        (CRIMSON, 'Crimson'),
        (PALE_VIOLET_RED, 'PaleVioletRed'),
        (ORANGE, 'Orange'),
        (DARK_KHAKI, 'DarkKhaki'),
        (VIOLET, 'Violet'),
        (CHOCOLATE, 'Chocolate'),
        (SILVER, 'Silver'),
        (LIME, 'Lime'),
        (DEEP_SKY_BLUE, 'DeepSkyBlue'),
        (OLIVE, 'Olive')
    )

    name = models.CharField(
        verbose_name='Название',
        max_length=254
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        choices=COLORS
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


class Amount(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients'
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_amount',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} ({self.amount}) in {self.recipe}'


class ShoppingCart(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='В корзине',
        related_name='in_shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} add to cart {self.recipe}'


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
        related_name='favorited'
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
