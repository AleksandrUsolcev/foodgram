from django.contrib import admin

from .models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'author')
    list_editable = ('name',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('created',)
# На странице рецепта вывести общее число добавлений этого рецепта в избранное.


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'count')
    list_filter = ('name',)
    ordering = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    ordering = ('id',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
