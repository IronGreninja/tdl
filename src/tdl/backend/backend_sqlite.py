import sqlite3
from contextlib import contextmanager
from dataclasses import astuple
from pathlib import Path

from .interface_backend import IBackend
from .models import ListEntry, get_Q_fields

Qfields, n_fields = get_Q_fields()


class Bsqlite(IBackend):
    table = "todolist"
    Q_select = f"SELECT {Qfields} FROM {table}"

    def __init__(self, data_dir: Path) -> None:
        self.datafile = data_dir / "tdl.db"
        super().__init__(self.datafile)  # creates parent if not exists

    def Insert(self, entry: ListEntry) -> None:
        _values = astuple(entry)
        placeholders = ",".join(["?"] * n_fields)
        Q = f"INSERT INTO {Bsqlite.table} ({Qfields}) VALUES ({placeholders})"
        with self.DBOpen() as cursor:
            cursor.execute(Q, _values)

    def Read(self, done: bool = False, priority: bool = False) -> list[ListEntry]:
        where = ""
        if done:
            where = "completed_on != ''"
        elif priority:
            where = "priority IS TRUE AND completed_on = ''"

        Q = Bsqlite.Q_select
        if where != "":
            Q += f" WHERE {where}"

        with self.DBOpen() as cursor:
            return cursor.execute(Q).fetchall()

    def MarkDone(self, id: int, completed_on: str) -> int:
        Q_check_if_done = f"""
            {Bsqlite.Q_select} where id = ? AND completed_on = '' 
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
        def mkListEntry(_, row):
            return ListEntry(*row)

        with sqlite3.connect(self.datafile) as connection:
            connection.row_factory = mkListEntry
            cursor = connection.cursor()
            cursor.execute(Q_create_table)
            yield cursor


Q_create_table = f"""
    CREATE TABLE IF NOT EXISTS {Bsqlite.table}(
       id INTEGER PRIMARY KEY,
       message TEXT NOT NULL,
       created_on TEXT NOT NULL,
       due_date TEXT,
       priority BOOLEAN,
       completed_on TEXT
    )
"""
