from api.models import Product, ProductImage, ProductInfoInCity
from django.contrib import admin
from django.forms import ModelForm, ValidationError


class ProductForm(ModelForm):
    def clean_discountPercent(self):
        value = self.cleaned_data['discountPercent']
        if not value <= 100:
            raise ValidationError("Максимальное значение скидки - 100%")
        return value


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    min_num = 1


class ProductInfoInCityInline(admin.StackedInline):
    model = ProductInfoInCity
    readonly_fields = ['price']
    min_num = 1
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['hideInMarket', 'showInMarket']

    list_display = [
        'id', 'name', 'article', 'isHiddenInMarket', 'category', 'weight']
    list_display_links = ['id', 'name']
    readonly_fields = ['id',  'createdAt', 'updatedAt']

    list_filter = ['category', 'isHiddenInMarket']
    search_fields = ['id', 'article', 'name', 'category__name', 'description']

    form = ProductForm
    inlines = [ProductImageInline, ProductInfoInCityInline]

    @admin.action(description="Снять блюдо с продажи", permissions=['change_hidden_in_market'])
    def hideInMarket(modeladmin, request, queryset):
        queryset.update(isHiddenInMarket=True)

    @admin.action(description="Разрешить продажу блюда", permissions=['change_hidden_in_market'])
    def showInMarket(modeladmin, request, queryset):
        queryset.update(isHiddenInMarket=False)

    def has_change_hidden_in_market_permission(self, request):
        return request.user.has_perm('api.change_hidden_in_market')
