import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .interface_backend import IBackend
from .models import ListEntry, get_fields

Rfields = get_fields()


class Bcsv(IBackend):
    def __init__(self, data_dir: Path) -> None:
        self.datafile = data_dir / "tdl.csv"
        self.todo_List = []
        super().__init__(self.datafile)  # creates parent if not exists
        if not self.datafile.exists():  # creates csvfile if not exists
            self.datafile.touch()
        else:
            with open(self.datafile, "r", newline="") as f:
                self.todo_List = list(csv.DictReader(f))

    def Insert(self, entry: ListEntry) -> None:
        entry.id = len(self.todo_List) + 1
        entry_dict = asdict(entry)
        self.todo_List.append(entry_dict)
        self.write_csvfile()

    def write_csvfile(self) -> None:
        with open(self.datafile, "w", newline="") as f:
            writer = csv.DictWriter(f, Rfields)
            writer.writeheader()
            writer.writerows(self.todo_List)

    def Read(self, ls_strat: str) -> list[ListEntry]:
        new_list: list[ListEntry] = []

        for entry in self.todo_List:
            _list_entry = self._mkListEntry(entry)
            isComplete: bool = _list_entry.completed_on != ""
            include = False

            if ls_strat == "done" and isComplete:
                include = True
            elif ls_strat == "priority" and _list_entry.priority and not isComplete:
                include = True
            elif ls_strat == "pending" and not isComplete:
                include = True
            elif ls_strat == "all":
                include = True

            if include:
                new_list.append(_list_entry)
        return new_list

    def _mkListEntry(self, E: dict[str, str | Any]) -> ListEntry:
        return ListEntry(
            id=int(E["id"]),
            priority={"False": False, "True": True}[E["priority"]],
            message=E["message"],
            created_on=E["created_on"],
            due_date=E["due_date"],
            completed_on=E["completed_on"],
        )

    def MarkDone(self, id: int, completed_on: str) -> int:
        try:
            if self.todo_List[id - 1]["completed_on"] != "":
                return 2
            else:
                self.todo_List[id - 1]["completed_on"] = completed_on
                self.write_csvfile()
                return 0
        except IndexError:
            return 1
