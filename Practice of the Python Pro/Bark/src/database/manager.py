from typing import Dict, List, Tuple
import sqlite3


class DatabaseManager(object):
    """Class for Persistence layer
    """

    def __init__(self, database_filename: str):

        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: Dict[str, Tuple[str, str]]):
        """
        CREATE TABLE IF NOT EXISTS bookmarks
        ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
          title TEXT NOT NULL, 
          url TEXT NOT NULL, 
          notes TEXT, 
          date_added TEXT NOT NULL );
        """
        columns_with_types_and_constraints = [
            f'{column_name} {data_type} {constraint}' for column_name, (data_type, constraint) in columns.items()]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types_and_constraints)});
            '''
        )

    def add(self, table_name: str, data: Dict[str, str]):
        """
        INSERT INTO bookmarks
        (title, url, notes, date_added) 
        VALUES (?, ?, ?, ?);
        """
        placeholders = ', '.join('?' * len(data))
        columns_names = ', '.join(list(data.keys()))
        columns_values = tuple(data.values())
        self._execute(
            f'''
            INSERT INTO {table_name}
            ({columns_names})
            VALUES ({placeholders});
            ''',
            columns_values
        )

    def delete(self, table_name: str, criteria: Dict[str, str]):
        """
        DELETE FROM bookmarks
        WHERE XXX AND YYY AND ZZZ
        """
        placeholders = [f'{column} = ?' for column in criteria]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values())
        )

    def select(self, table_name: str, criteria: Dict[str, str] = None, order_by: str = None):
        """
        SELECT * FROM bookmarks
        WHERE XXX = ?
        ORDER BY YYY;
        """
        query = f'SELECT * FROM {table_name}'
        criteria = criteria or dict()
        
        if len(criteria) != 0:
            placeholders = [f'{column} = ?' for column in criteria]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by is not None:
            query += f' ORDER BY {order_by}'

        return self._execute(
            query,
            tuple(criteria.values())
        )