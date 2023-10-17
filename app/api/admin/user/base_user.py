from api.models import BaseUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    actions = [
        'changeToStaff', 'changeToSimpleUser',
        'disableAccount', 'enableAccount']
    fieldsets = (
        (None, {"fields": ("username", "password", 'id',)}),
        (_("Important dates"), {"fields": ("last_login", "createdAt")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    readonly_fields = ['id', "createdAt"]
    list_display = ['id', 'username', 'is_staff', 'is_superuser']
    search_fields = ['id', 'username']
    list_display_links = ['id', 'username']

    @admin.action(description="Назначить роль персонала", permissions=['super_user'])
    def changeToStaff(modeladmin, request, queryset):
        queryset.update(is_staff=True)

    @admin.action(description="Убрать роль персонала", permissions=['super_user'])
    def changeToSimpleUser(modeladmin, request, queryset):
        queryset.update(is_staff=False)

    @admin.action(description="Отключить аккаунт", permissions=['super_user'])
    def disableAccount(modeladmin, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Включить аккаунт", permissions=['super_user'])
    def enableAccount(modeladmin, request, queryset):
        queryset.update(is_active=True)

    def has_super_user_permission(self, request):
        return request.user.is_superuser
