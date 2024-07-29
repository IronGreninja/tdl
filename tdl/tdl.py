import csv
from datetime import date
from pathlib import Path

from rich import print

priority_str = {1: "[green]!  [/]", 2: "[blue]!! [/]", 3: "[red]!!![/]"}


class TDL:

    fields = ("date", "priority", "message")

    def __init__(self, file: Path | None = None) -> None:
        self.DATA_FILE = file or (Path.home() / ".tdl/list.csv")
        self.new_list = False
        if not self.DATA_FILE.parent.exists():
            self.DATA_FILE.mkdir()
        if not self.DATA_FILE.exists():
            with open(self.DATA_FILE, "w", newline="") as f:
                csv.DictWriter(f, TDL.fields).writeheader()
            self.new_list = True

    def add_item(self, priority: int, message: str) -> None:
        date_today = str(date.today())
        csv_row = dict(zip(TDL.fields, (date_today, priority, message)))
        with open(self.DATA_FILE, "a", newline="") as f:
            csv.DictWriter(f, TDL.fields).writerow(csv_row)

    def show_list(self, sort_by: str, show_index: bool = False) -> list:
        if self.new_list:
            print("ToDo list empty")
            return []
        with open(self.DATA_FILE, "r", newline="") as f:
            todo_items = list(csv.DictReader(f))
        if len(todo_items) == 0:
            print("ToDo list empty")
            return []
        if sort_by == "n":
            todo_items.reverse()
        elif sort_by == "p":
            todo_items.sort(reverse=True, key=lambda item: item["priority"])

        curr_year = str(date.today().year)
        for index, item in enumerate(todo_items):
            item_date, priority, msg = item.values()

            if show_index:
                print(f"{index})  ", end="")
            if curr_year == item_date[:4]:
                item_date = item_date[5:]  # remove year from date str
            print(rf"\[{item_date}] {priority_str[int(priority)]}  -  {msg}")

        return todo_items

    def delete_item(self, sort_by: str) -> None:
        # TODO: implement other sort_by options
        todo_items = self.show_list(sort_by="o", show_index=True)
        if len(todo_items) == 0:
            return
        print(
            "Enter index number(s) separated with a space to delete(empty to cancel): ",
            end="",
        )
        inp = input()
        if inp == "":
            return

        # delete indexes and writeback
        indexes = list(map(int, inp.split()))
        for i in sorted(indexes, reverse=True):
            if 0 <= i and i <= len(todo_items) - 1:
                del todo_items[i]
            else:
                print("Invalid index(es) encountered. Aborting")
                return
        with open(self.DATA_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, TDL.fields)
            writer.writeheader()
            writer.writerows(todo_items)
