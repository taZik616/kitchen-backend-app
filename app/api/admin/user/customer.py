from api.json_form_schema import COORDINATES_SCHEMA
from api.models import BasketProduct, Customer, CustomerAddress
from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_jsonform.widgets import JSONFormWidget


class BasketProductInline(admin.StackedInline):
    model = BasketProduct
    extra = 1
    autocomplete_fields = ['product']


class CustomerAddressForm(ModelForm):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        widgets = {
            'coords': JSONFormWidget(schema=COORDINATES_SCHEMA),
        }


class CustomerAddressInline(admin.StackedInline):
    model = CustomerAddress
    extra = 1
    autocomplete_fields = ['city']

    fieldsets = [
        [None, {
            'fields': ['city', 'customer']
        }],
        ['Данные местоположения', {
            'fields': ['streetAndHouse', 'entrance', 'floor', 'flat', 'comment', 'coords']
        }],
    ]

    form = CustomerAddressForm


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    model = CustomerAddress
    search_fields = [
        'customer__id', 'customer__user__username', 'streetAndHouse', 'city__name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    actions = ['setPhoneVerified', 'setPhoneNotVerified']
    list_display = [
        'id', 'user', 'name', 'isPhoneNumberVerified', 'city']
    fieldsets = (
        [None, {
            'fields': ['user', 'city', 'isPhoneNumberVerified', 'bonuses', 'defaultAddress']
        }],
        ['Персональная информация', {
            'fields': ['name', 'awaitingDeletion', 'deletionStartDate']
        }],
    )
    autocomplete_fields = ['defaultAddress']
    list_display_links = ['id', 'user']
    readonly_fields = ['id']
    list_filter = ['city']
    search_fields = ["user__username", "name"]
    inlines = [BasketProductInline, CustomerAddressInline]

    @admin.action(description="Подтвердить номер телефона", permissions=['super_user'])
    def setPhoneVerified(modeladmin, request, queryset):
        queryset.update(isPhoneNumberVerified=True)

    @admin.action(description="Убрать подтвержденный статус у телефона", permissions=['super_user'])
    def setPhoneNotVerified(modeladmin, request, queryset):
        queryset.update(isPhoneNumberVerified=False)

    def has_super_user_permission(self, request):
        return request.user.is_superuser
