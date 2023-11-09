from api.json_form_schema import ADDRESS_SCHEMA
from api.models import Order, OrderProduct
from django.contrib import admin
from django.forms import ModelForm
from django_jsonform.widgets import JSONFormWidget


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 1
    min_num = 1
    readonly_fields = ['id']


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    search_fields = [
        'product__name', 'order__id', 'order__customer__user__username']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'address': JSONFormWidget(schema=ADDRESS_SCHEMA),
        }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'status', 'paymentMethod', 'cityName', 'customer', 'totalPrice']
    list_display_links = ['id', 'status']

    fieldsets = [
        [None, {
            'fields': [
                'customer', 'city', 'status', 'paymentMethod', 'address'
            ]
        }],
        ['Дополнительная информация', {
            'fields': ['id', 'totalPrice', 'createdAt', 'updatedAt']
        }]
    ]
    readonly_fields = ['id', 'createdAt', 'updatedAt', 'totalPrice']

    ordering = ['-createdAt']
    search_fields = ['id', 'locality__name', 'customer__user__username']

    inlines = [OrderProductInline]
    form = OrderForm

    @admin.display(description='Итого')
    def totalPrice(self, obj):
        return obj.totalPrice

    @admin.display(description='Город')
    def cityName(self, obj):
        return obj.city.name if obj.city else '<None>'
