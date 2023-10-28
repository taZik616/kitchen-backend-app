from api.models import SupportRequest
from django.contrib import admin


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']
    readonly_fields = ['id', 'createdAt']
    ordering = ['-createdAt']
    search_fields = [
        'id', 'customer__user__username', 'customer__name', 'message']
