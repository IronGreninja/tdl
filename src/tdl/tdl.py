import tomllib
from argparse import Namespace
from pathlib import Path

import arrow

from .backend import Backend
from .backend.models import ListEntry
from .display import DisplayList, console

DT_format = "YYYY-MM-DD HH:mm:ss ZZZ"


def timestamp():
    return arrow.now().format(DT_format)


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

    def add_item(self) -> None:
        entry = ListEntry(
            id=None,
            message=self.args.message,
            created_on=timestamp(),
            due_date="",
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
        console.print("[bold red]Not Implemented")
