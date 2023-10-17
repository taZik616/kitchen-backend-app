from api.models import HelpfulInfo, ServerSetting
from django.contrib import admin
from django.forms import ModelForm
from floppyforms.widgets import Input

HELPFUL_INFO_KEYS = ['legalInfo', 'about', 'support']
HELPFUL_INFO_TITLES = ['Правовая информация', 'О нас', 'Поддержка']


class HelpfulInfoForm(ModelForm):
    class Meta:
        model = HelpfulInfo
        fields = "__all__"
        widgets = {
            'key': Input(datalist=HELPFUL_INFO_KEYS),
            'title': Input(datalist=HELPFUL_INFO_TITLES)
        }


class HelpfulInfoInline(admin.StackedInline):
    model = HelpfulInfo
    form = HelpfulInfoForm
    extra = 1


@admin.register(ServerSetting)
class ServerSettingAdmin(admin.ModelAdmin):
    inlines = [HelpfulInfoInline]
