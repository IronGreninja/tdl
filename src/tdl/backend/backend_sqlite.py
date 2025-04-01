import sqlite3
from contextlib import contextmanager
from pathlib import Path
from .models import ListEntry, ListEntry_R
from dataclasses import fields, astuple

from .interface_backend import IBackend


class Bsqlite(IBackend):
    table = "todolist"

    def __init__(self, data_dir: Path) -> None:
        self.datafile = data_dir / "tdl.db"
        super().__init__(self.datafile)  # creates parent if not exists

    @staticmethod
    def get_fields(id: bool = False) -> tuple[str, int]:
        _fields = fields(ListEntry_R if id else ListEntry)
        _Qfields = ",".join(f.name for f in _fields)
        return (_Qfields, len(_fields))

    def Insert(self, entry: ListEntry) -> None:
        _values = astuple(entry)
        _Qfields, _flen = Bsqlite.get_fields()
        placeholders = ",".join(["?"] * _flen)
        Q = f"INSERT INTO {Bsqlite.table} ({_Qfields}) VALUES ({placeholders})"
        with self.DBOpen() as cursor:
            cursor.execute(Q, _values)

    def Read(self, done: bool = False, priority: bool = False) -> list[ListEntry_R]:
        # columns = "id, priority, message, createdOn"
        # where = ""
        # if done:
        #     columns += ", completedOn"
        #     where += "completedOn IS NOT NULL "
        #     if priority:
        #         where += "AND priority = 1"
        # elif priority:
        #     where += "priority = 1 AND completedOn IS NULL"
        # else:
        #     where += "completedOn IS NULL"

        where = ""
        if done:
            where = "completed_on != ''"
        elif priority:
            where = "priority IS TRUE"

        _Qfields, _ = Bsqlite.get_fields(id=True)
        Q = f"SELECT {_Qfields} FROM {Bsqlite.table}"
        if where != "":
            Q += f" WHERE {where}"

        with self.DBOpen() as cursor:
            return cursor.execute(Q).fetchall()

    def MarkDone(self, id: int, completed_on: str) -> int:
        _Qfields, _ = Bsqlite.get_fields(id=True)
        Q_check_if_done = f"""
            SELECT {_Qfields} FROM {Bsqlite.table} where id = ? AND completed_on = '' 
        """
        Q_mark_done = f"""
            UPDATE {Bsqlite.table} SET completed_on = ? WHERE id = ?
        """
        with self.DBOpen() as cursor:
            id_id = cursor.execute(Q_check_if_done, (id,)).fetchone()
            if id_id is None:
                return 2
            cursor.execute(Q_mark_done, (completed_on, id))
            if cursor.rowcount == 0:
                return 1
            else:
                return 0

    @contextmanager
    def DBOpen(self):
        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}

        def mkListEntry_R(_, row):
            # BUG: this is most likely wrong
            return ListEntry_R(*row)

        with sqlite3.connect(self.datafile) as connection:
            connection.row_factory = mkListEntry_R
            cursor = connection.cursor()
            cursor.execute(Q_create_table)
            yield cursor


Q_create_table = f"""
    CREATE TABLE IF NOT EXISTS {Bsqlite.table}(
       id INTEGER PRIMARY KEY NOT NULL,
       message TEXT NOT NULL,
       created_on TEXT NOT NULL,
       due_date TEXT,
       priority BOOLEAN,
       completed_on TEXT
    )
"""
