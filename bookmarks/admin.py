from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from .models import Label, Bookmark


class BaseModelAdmin(admin.ModelAdmin):

    # Show most recent objects first.
    ordering = ['-id']

    # The default value is '-'.
    empty_value_display = ''

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        # Make all list_display fields clickable.
        self.list_display_links = self.list_display


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
