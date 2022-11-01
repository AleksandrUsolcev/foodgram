from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Subscribe, User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff')
    list_editable = ('is_staff',)
    list_filter = ('username', 'email')
    ordering = ('id',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'author')
    ordering = ('date',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
