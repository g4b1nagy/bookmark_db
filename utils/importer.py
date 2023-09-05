import base64
import datetime
import pathlib

from bs4 import BeautifulSoup


class ImporterException(Exception):
    pass


def get_datetime(timestamp):
    timestamp = int(timestamp)
    if timestamp == 0:
        return None
    else:
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)


def get_bytes(icon):
    if icon is None:
        return None
    else:
        data = icon.split('base64,')[1]
        data = base64.b64decode(data)
        return data


def parse_html(html, bookmarks=None, labels=None, current_labels=None):
    if bookmarks is None:
        bookmarks = {}
    if labels is None:
        labels = {}
    if current_labels is None:
        current_labels = set()
    for child in getattr(html, 'children', []):
        label = child.find('h3')

        # If we encountered a bookmark.
        if child.name == 'a':
            add_date = child.attrs.get('add_date')
            icon = child.attrs.get('icon')
            name = child.string
            url = child.attrs.get('href')
            if name is None:
                name = url
            if url not in bookmarks:
                bookmarks[url] = {
                    # Only use the first add_date.
                    'add_date': add_date,
                }
            # Fill in any missing information.
            if bookmarks[url]['add_date'] == '0' and add_date != '0':
                bookmarks[url]['add_date'] = add_date
            # Always update the rest of the attributes.
            bookmarks[url]['icon'] = icon
            bookmarks[url]['name'] = name
            if 'labels' not in bookmarks[url]:
                bookmarks[url]['labels'] = set()
            bookmarks[url]['labels'].update(current_labels)

        # If we encountered a folder with a non-empty name.
        elif child.name == 'dt' and label is not None and label.string is not None:
            add_date = label.attrs.get('add_date')
            last_modified = label.attrs.get('last_modified')
            name = label.string
            if name not in labels:
                labels[name] = {
                    # Only use the first add_date and last_modified.
                    'add_date': add_date,
                    'last_modified': last_modified,
                }
            # Fill in any missing information.
            if labels[name]['add_date'] == '0' and add_date != '0':
                labels[name]['add_date'] = add_date
            if labels[name]['last_modified'] == '0' and last_modified != '0':
                labels[name]['last_modified'] = last_modified
            parse_html(child, bookmarks, labels, current_labels.union([name]))
        else:
            parse_html(child, bookmarks, labels, current_labels)
    return bookmarks, labels


def get_bookmarks_and_labels(path):
    path = pathlib.Path(path)
    if not path.exists():
        raise ImporterException(f'Path does not exist: {path}')
    if path.is_file():
        file_paths = [path]
    elif path.is_dir():
        file_paths = path.glob('**/*')
    else:
        raise ImporterException(f'Path is neither file nor dir: {path}')
    file_paths = sorted([x for x in file_paths if x.is_file() and x.suffix.lower() == '.html'])
    if len(file_paths) == 0:
        raise ImporterException(f'No .html files found at: {path}')
    bookmarks = {}
    labels = {}
    for file_path in file_paths:
        print(file_path)
        with file_path.open() as file:
            html = BeautifulSoup(file, 'html5lib')
        parse_html(html, bookmarks, labels)
    return bookmarks, labels
