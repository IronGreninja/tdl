import tomllib
from pathlib import Path

import arrow

from .backend import Backend
from .backend.models import ListEntry
from .display import DisplayList, console

DT_format = "YYYY-MM-DD HH:mm:ss ZZZ"


def timestamp():
    return arrow.now().format(DT_format)


class TDL:
    def __init__(self) -> None:
        base_dir = Path.home() / ".tdl"
        cfg_path = base_dir / ".config.toml"

        if cfg_path.is_file():
            with open(cfg_path, "rb") as f:
                self.cfg: dict = tomllib.load(f)
        else:
            self.cfg = {}

        if f := self.cfg.get("data_dir"):
            data_dir = Path(f).expanduser()
        else:
            data_dir = base_dir
        try:
            self.backend = Backend[self.cfg.get("backend") or "sqlite"](data_dir)
        except KeyError:
            raise NotImplementedError("backend not supported")

    def add_item(self, priority: bool, message: str) -> None:
        entry = ListEntry(
            id=None,
            message=message,
            created_on=timestamp(),
            due_date="",
            priority=priority,
            completed_on="",
        )
        self.backend.Insert(entry)

    def show_list(self, priority: bool, done: bool) -> None:
        todolist: list[ListEntry] = self.backend.Read(done, priority)

        if len(todolist) == 0:
            console.print("!!ToDo List empty!!")
            return
        DisplayList(
            todoList=todolist,
            style=self.cfg.get("style"),
        )()

    def mark_done_item(self, id: int) -> None:
        err = self.backend.MarkDone(id, timestamp())
        err_map = {
            0: "id updated successfully",
            1: "id does not exist",
            2: "id already marked as complete",
        }
        console.print(err_map[err])
