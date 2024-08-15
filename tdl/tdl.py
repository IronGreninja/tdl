import csv
from datetime import datetime as DT
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


class TDL:

    fields = ("ID", "Message", "CreatedOn", "CompletedOn", "Priority")

    def __init__(self, file: Path | None = None) -> None:
        self.DATA_FILE = file or (Path.home() / ".tdl/list.csv")
        self.todolist = []
        if not self.DATA_FILE.parent.exists():
            self.DATA_FILE.parent.mkdir()
        if not self.DATA_FILE.exists():
            self.DATA_FILE.touch()
        else:
            with open(self.DATA_FILE, "r", newline="") as f:
                self.todolist = list(csv.DictReader(f))

    def write_csvfile(self) -> None:
        with open(self.DATA_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, TDL.fields)
            writer.writeheader()
            writer.writerows(self.todolist)

    def add_item(self, priority: bool, message: str) -> None:
        DT_now = str(DT.today())
        new_id = len(self.todolist) + 1
        field_val_zip = zip(TDL.fields, (new_id, message, DT_now, None, priority))
        csv_row = dict(field_val_zip)
        self.todolist.append(csv_row)
        self.write_csvfile()

    def show_list(self, priority: bool, showAll: bool) -> None:
        if len(self.todolist) == 0:
            console.print("ToDo list empty")
            return

        table = Table(*TDL.fields[:3], box=box.SIMPLE_HEAD)
        if showAll:
            table.add_column(TDL.fields[3])  # add CompletedOn
        for item_row in self.todolist:
            row = list(item_row.values())

            if priority and row[-1] == "False":
                continue

            if (
                not showAll and row[3] != ""
            ):  # skip if showAll is False and CompletedOn str is not empty (i.e, item is completed)
                continue

            if row[-1] == "True":  # priority is True
                row[0] = f"[red]{row[0]}[/]"  # red id color is priority item
            table.add_row(*row[:-1])  # dont add priority
        console.print(table)

    def mark_done_item(self, id: int) -> None:
        try:
            if self.todolist[id - 1]["CompletedOn"] != "":
                console.print("Item alreadey marked as Completed")
            else:
                DT_now = str(DT.today())
                self.todolist[id - 1]["CompletedOn"] = DT_now
                self.write_csvfile()
        except IndexError:
            console.print(f"Invalid ID {id}")
