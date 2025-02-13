from django.contrib import admin

from movies_api.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)
