import tomllib
from pathlib import Path

import arrow
from rich import box
from rich.console import Console
from rich.table import Table

from .backend import Backend
from .backend.models import ListEntry, ListEntry_R

console = Console()
DT_format = "YYYY-MM-DD HH:mm:ss ZZZ"


def timestamp():
    return arrow.now().format(DT_format)


class TDL:
    def __init__(self, file: Path | None = None) -> None:
        base_dir = Path.home() / ".tdl"
        cfg_path = base_dir / ".config.toml"

        if cfg_path.is_file():
            with open(cfg_path, "rb") as f:
                cfg: dict = tomllib.load(f)
        else:
            cfg = {}

        if f := cfg.get("data_dir"):
            data_dir = Path(f).expanduser()
        else:
            data_dir = base_dir
        try:
            self.backend = Backend[cfg.get("backend") or "sqlite"](data_dir)
        except KeyError:
            raise NotImplementedError("backend not supported")

    def add_item(self, priority: bool, message: str) -> None:
        self.backend.Insert(ListEntry(message, timestamp(), "", priority, ""))

    def show_list(self, priority: bool, done: bool) -> None:
        todolist: list[ListEntry_R] = self.backend.Read(done, priority)

        if len(todolist) == 0:
            console.print("ToDo list empty")
            return

        from pprint import pp

        pp(todolist)

        # columns = list(todolist[0].keys())
        #
        # table = Table(*columns, box=box.SIMPLE_HEAD)
        #
        # for row in todolist:
        #     values = list(row.values())
        #     table.add_row(str(values[0]), str(values[1]), *values[2:])
        # console.print(table)

    def mark_done_item(self, id: int) -> None:
        err = self.backend.MarkDone(id, timestamp())
        err_map = {
            0: "id updated successfully",
            1: "id does not exist",
            2: "id already marked as complete",
        }
        console.print(err_map[err])
