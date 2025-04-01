import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .interface_backend import IBackend


class Bsqlite(IBackend):

    def __init__(self, datafile: Path | None = None) -> None:
        self.datafile: Path = datafile or (Path.home() / ".tdl/tdl.db")
        super().__init__(self.datafile)  # creates parent if not exists

    def Insert(self, message: str, createdOn: str, priority: int) -> None:
        with self.DBOpen() as cursor:
            cursor.execute(insert_q, (message, createdOn, priority))

    def Read(
        self, done: bool = False, priority: bool = False
    ) -> list[dict[str, str | None | int]]:

        columns = "id, priority, message, createdOn"
        where = ""
        if done:
            columns += ", completedOn"
            where += "completedOn IS NOT NULL "
            if priority:
                where += "AND priority = 1"
        elif priority:
            where += "priority = 1 AND completedOn IS NULL"
        else:
            where += "completedOn IS NULL"

        query = f"SELECT {columns} FROM todolist"
        if where != "":
            query += f" WHERE {where}"

        # print(query)
        with self.DBOpen() as cursor:
            return cursor.execute(query).fetchall()

    def MarkDone(self, id: int, completedOn: str) -> int:
        with self.DBOpen() as cursor:
            # returns {id: id} if id is not already marked completed
            # returns None if its already marked as complete
            id_id = cursor.execute(check_if_done_q, (id,)).fetchone()
            if id_id is None:
                return 2
            cursor.execute(mark_done_q, (completedOn, id))
            if cursor.rowcount == 0:
                return 1
            else:
                return 0

    @contextmanager
    def DBOpen(self):

        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}

        with sqlite3.connect(self.datafile) as connection:
            connection.row_factory = dict_factory
            cursor = connection.cursor()
            cursor.execute(create_table_q)
            yield cursor


create_table_q = """
    CREATE TABLE IF NOT EXISTS todolist(
       id INTEGER PRIMARY KEY NOT NULL,
       priority INTEGER,
       message TEXT NOT NULL,
       createdOn TEXT NOT NULL,
       completedOn TEXT
    )
"""

insert_q = """
    INSERT INTO todolist (message, createdOn, priority) VALUES (?, ?, ?)
"""

mark_done_q = """
    UPDATE todolist SET completedOn = ? WHERE id = ?
"""

check_if_done_q = """
    SELECT id FROM todolist where id = ? AND completedOn IS NULL
"""
