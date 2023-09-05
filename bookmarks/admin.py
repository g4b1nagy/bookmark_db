from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from utils.admin import BaseModelAdmin

from .models import Label, Bookmark


@admin.register(Label)
class LabelAdmin(BaseModelAdmin):
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
    ]
    readonly_fields = [
        'created_on',
        'updated_on',
    ]


@admin.register(Bookmark)
class BookmarkAdmin(BaseModelAdmin):
    search_fields = [
        'name',
        'url',
        'labels__name',
    ]
    list_display = [
        '_icon',
        'name',
        'url',
    ]
    list_filter = [
        'labels__name',
    ]
    readonly_fields = [
        'created_on',
        'updated_on',
    ]
    autocomplete_fields = [
        'labels',
    ]

    @admin.display(description=_('icon'))
    def _icon(self, obj):
        if obj.icon.name == '':
            url = ''
        else:
            url = obj.icon.url
        return format_html('<img style="width: auto; max-height: 16px;" src="{url}">', url=url)
