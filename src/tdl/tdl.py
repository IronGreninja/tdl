import tomllib
from argparse import Namespace
from pathlib import Path

import arrow

from .backend import Backend
from .backend.models import ListEntry
from .display import DisplayList, console


def timestamp():
    return arrow.now().format()


class TDL:
    def __init__(self, args: Namespace) -> None:
        self.args = args

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

    def __call__(self) -> None:
        {
            "do": self.add_item,
            "ls": self.show_list,
            "done": self.mark_done_item,
            "clear": self.clear_done,
        }[self.args.command]()

    def _parseDueDate(self) -> str:
        if not self.args.due_date:
            return ""
        import re

        pattern = re.compile(r"((\d+)d)?((\d+)h)?")  # [1]: days, [3]: hours
        match = pattern.fullmatch(self.args.due_date)
        if not match:
            raise Exception("Can't parse Due Date")
        grps = match.groups()
        if grps[0] is None and grps[2] is None:
            return ""
        days = int(grps[1]) if grps[1] else 0
        hrs = int(grps[3]) if grps[3] else 0
        due_date_str = arrow.now().shift(days=days, hours=hrs).format()
        console.print(due_date_str)
        return due_date_str

    def add_item(self) -> None:
        entry = ListEntry(
            id=None,
            message=self.args.message,
            created_on=timestamp(),
            due_date=self._parseDueDate(),
            priority=self.args.priority,
            completed_on="",
        )
        self.backend.Insert(entry)

    def show_list(self) -> None:
        a = self.args
        if a.done:
            ls_strat = "done"
        elif a.priority:
            ls_strat = "priority"
        elif a.all:
            ls_strat = "all"
        else:
            ls_strat = "pending"

        todolist: list[ListEntry] = self.backend.Read(ls_strat)

        if len(todolist) == 0:
            if ls_strat == "all":
                console.print("!!ToDo List empty!!")
            else:
                console.print(f"!!No {ls_strat} items!!")
            return

        DisplayList(
            todoList=todolist,
            style=self.cfg.get("style"),
            timestamp_format=self.cfg.get("timestamp_format", "ddd, D/MMM/YY"),
            humanize=self.cfg.get("due_date_humanize", False),
        )()

    def mark_done_item(self) -> None:
        err = self.backend.MarkDone(self.args.id, timestamp())
        err_map = {
            0: "id updated successfully",
            1: "id does not exist",
            2: "id already marked as complete",
        }
        console.print(err_map[err])

    def clear_done(self):
        self.backend.ClearDone()
