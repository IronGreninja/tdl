import csv
import os
import tomllib
from pathlib import Path
from platform import system

import arrow
from rich import box
from rich.console import Console
from rich.table import Table

from .backend import Backend

console = Console()
DT_format = "YYYY-MM-DD HH:mm:ss ZZZ"


class TDL:

    fields = ("ID", "Message", "CreatedOn", "CompletedOn", "Priority")

    def __init__(self, file: Path | None = None) -> None:
        os_name = system()
        settings = {}
        if os_name == "Linux":
            config = (
                Path(os.getenv("XDG_CONFIG_HOME") or (os.getenv("HOME") + "/.config"))
                / "tdl/tdl.toml"
            )
        else:
            raise NotImplementedError("os not supported")
        if config.is_file():
            with open(config, "rb") as f:
                settings = tomllib.load(f)

        datafile = None
        if f := settings.get("data_dir"):
            datafile = Path(f).expanduser() / "tdl.db"
        try:
            self.backend = Backend[settings.get("backend") or "sqlite"](datafile)
        except KeyError:
            raise NotImplementedError("backend not supported")

    def add_item(self, priority: bool, message: str) -> None:
        DT_now = arrow.now().format(DT_format)
        P = {True: 1, False: 0}
        self.backend.Insert(message=message, createdOn=DT_now, priority=P[priority])

    def show_list(self, priority: bool, done: bool) -> None:
        todolist: list[dict[str, int | str]] = self.backend.Read(
            priority=priority, done=done
        )
        if len(todolist) == 0:
            console.print("ToDo list empty")
            return

        columns = list(todolist[0].keys())

        table = Table(*columns, box=box.SIMPLE_HEAD)

        for row in todolist:
            values = list(row.values())
            table.add_row(str(values[0]), str(values[1]), *values[2:])
        console.print(table)

    def mark_done_item(self, id: int) -> None:
        DT_now = arrow.now().format(DT_format)
        err = self.backend.MarkDone(id=id, completedOn=DT_now)
        if err == 0:
            console.print("id updated successfully")
        elif err == 1:
            console.print("id does not exist")
        elif err == 2:
            console.print("id already marked as complete")
