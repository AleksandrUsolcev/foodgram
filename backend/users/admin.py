from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'role')
    list_editable = ('role',)
    list_filter = ('role', 'username', 'email')
    ordering = ('id',)


admin.site.register(User, UserAdmin)
