from django.contrib import admin

from .models import Amount, Favorite, Ingredient, Recipe, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'author', 'favorited_count')
    list_editable = ('name',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('created',)
    readonly_fields = ('favorited_count',)

    def favorited_count(self, obj):
        return obj.favorited.count()

    favorited_count.short_description = 'В избранном'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    ordering = ('id',)


class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'ingredient', 'recipe')
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
admin.site.register(Amount, AmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
