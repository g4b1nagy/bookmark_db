import hashlib

from django.conf import settings
from django.core.management.base import BaseCommand

from bookmarks.models import Bookmark, Label
from utils.importer import get_bookmarks_and_labels, get_datetime, get_bytes


class Command(BaseCommand):
    help = 'Import bookmarks from .html files.'

    def add_arguments(self, parser):
        parser.add_argument('bookmark_path', type=str, help='Path to bookmark file or to directory containing bookmark files.')

    def handle(self, *args, **options):
        bookmarks, labels = get_bookmarks_and_labels(options['bookmark_path'])
        for label_name, label_data in labels.items():
            label, created = Label.objects.update_or_create(
                name=label_name,
                defaults={
                    'created_on': get_datetime(label_data['add_date']),
                    'updated_on': get_datetime(label_data['last_modified']),
                },
            )
            labels[label_name]['id'] = label.id
        for bookmark_url, bookmark_data in bookmarks.items():
            if len(bookmark_url) > Bookmark.url.field.max_length:
                print(f'URL too long, skipping: {bookmark_url}')
                continue
            bookmark, created = Bookmark.objects.update_or_create(
                url=bookmark_url,
                defaults={
                    'created_on': get_datetime(bookmark_data['add_date']),
                    'name': bookmark_data['name'],
                },
            )
            if bookmark_data['icon'] is not None:
                icon = get_bytes(bookmark_data['icon'])
                digest = hashlib.md5(icon).hexdigest()
                filename = f'{digest}.png'
                with open(settings.MEDIA_ROOT / filename, 'wb') as file:
                    file.write(icon)
                bookmark.icon = filename
                bookmark.save()
            bookmark.labels.add(*[labels[x]['id'] for x in bookmark_data['labels']])
