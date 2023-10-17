from api.json_form_schema import COORDINATES_SCHEMA
from api.models import City
from django.contrib import admin
from django.forms import ModelForm
from django_jsonform.widgets import JSONFormWidget


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'
        widgets = {
            'coordinates': JSONFormWidget(schema=COORDINATES_SCHEMA),
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityForm
    list_display = ['id', 'name', 'phoneNumber', 'officeAddress']
    readonly_fields = ['id']
    ordering = ['-id']
    search_fields = ['name', 'officeAddress', 'phoneNumber']
