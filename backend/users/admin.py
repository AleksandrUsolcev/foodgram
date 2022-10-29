from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'role')
    list_editable = ('role',)
    list_filter = ('role', 'username', 'email')
    ordering = ('id',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'author', 'id')
    ordering = ('date',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
