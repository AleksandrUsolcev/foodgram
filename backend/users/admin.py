from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'recipes_count', 'subscribers_count',)
    list_filter = ('username', 'email')
    ordering = ('id',)

    def recipes_count(self, obj):
        return obj.recipes.count()

    def subscribers_count(self, obj):
        return obj.subscribers.count()

    recipes_count.short_description = 'Рецептов'
    subscribers_count.short_description = 'Подписчиков'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'author')
    ordering = ('date',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
