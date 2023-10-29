from api.models import BasketProduct, Customer
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BasketProductInline(admin.StackedInline):
    model = BasketProduct
    extra = 1
    autocomplete_fields = ['product']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    actions = ['setPhoneVerified', 'setPhoneNotVerified']
    list_display = [
        'id', 'user', 'name', 'isPhoneNumberVerified', 'city']
    fieldsets = (
        (None, {'fields': ('user', 'city', 'isPhoneNumberVerified', 'bonuses')}),
        ('Персональная информация', {
         "fields": ['name', 'awaitingDeletion', 'deletionStartDate']}),
    )
    list_display_links = ['id', 'user']
    readonly_fields = ['id']
    list_filter = ['city']
    search_fields = ["user__username", "name"]
    inlines = [BasketProductInline]

    @admin.action(description="Подтвердить номер телефона", permissions=['super_user'])
    def setPhoneVerified(modeladmin, request, queryset):
        queryset.update(isPhoneNumberVerified=True)

    @admin.action(description="Убрать подтвержденный статус у телефона", permissions=['super_user'])
    def setPhoneNotVerified(modeladmin, request, queryset):
        queryset.update(isPhoneNumberVerified=False)

    def has_super_user_permission(self, request):
        return request.user.is_superuser
