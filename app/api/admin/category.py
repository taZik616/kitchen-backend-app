from api.models import Category
from django.contrib import admin
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_html_previewImage', 'slug']
    ordering = ['name']
    search_fields = ['id', 'name']
    list_per_page = 150
    fields = [
        'id', 'name', 'slug', 'previewImage', 'get_html_previewImage']
    readonly_fields = ['id', 'get_html_previewImage']
    prepopulated_fields = {"slug": ["name"]}

    def get_html_previewImage(self, object):
        if object.previewImage:
            return mark_safe(f"<img src='{object.previewImage.url}' width=50>")

    get_html_previewImage.short_description = "Картинка"
