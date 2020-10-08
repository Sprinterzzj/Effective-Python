from datetime import datetime
from typing import Dict, List, Tuple
import sys

from ..database.manager import DatabaseManager


"""
Classes for bussiness logic layer, all classes must implement a execute method.
"""
# sqlite2 will automatically create this database file if it does not exist.
DB = DatabaseManager('bookmarks.db')
TABLE_NAME = 'bookmarks'


class CreateBookmarksTable(object):
    COLUMNS = {'id': ('integer', 'primary key autoincrement'),
               'title': ('text', 'not null'),
               'url': ('text', 'not null'),
               'notes': ('text', ''),
               'date_added': ('text', 'not null')}

    def execute(self):
        DB.create_table(table_name=TABLE_NAME, columns=self.__class__.COLUMNS)


class AddBookmark(object):
    def execute(self, data: Dict[str, str]):
        data.update({'date_added': datetime.utcnow().isoformat()})
        DB.add(table_name=TABLE_NAME, data=data)


class ListBookmarks(object):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return DB.select(table_name=TABLE_NAME, order_by=self.order_by).fetchall()


class DeleteBookmark(object):
    def execute(self, bookmark_id: str):
        DB.delete(table_name=TABLE_NAME, criteria={'id': bookmark_id})
        return 'Bookmark deleted !'


class Quit(object):
    def execute(self):
        sys.exit()
