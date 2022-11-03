from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'author')
    list_editable = ('name',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('created',)
# На странице рецепта вывести общее число добавлений этого рецепта в избранное.


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'amount')
    list_filter = ('name',)
    ordering = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    ordering = ('id',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    ordering = ('user',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    ordering = ('user',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
