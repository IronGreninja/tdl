import csv
from pathlib import Path
from typing import Dict, List

from .interface_backend import IBackend


class Bcsv(IBackend):
    fields = ("id", "priority", "message", "createdOn", "completedOn")

    def __init__(self, datafile: Path | None = None) -> None:
        self.datafile = datafile or (Path.home() / ".tdl/tdl.csv")
        self.todo_List = []
        super().__init__(self.datafile)  # creates parent if not exists
        if not self.datafile.exists():  # creates csvfile if not exists
            self.datafile.touch()
        else:
            with open(self.datafile, "r", newline="") as f:
                self.todo_List = list(csv.DictReader(f))

    def Insert(self, message: str, createdOn: str, priority: int) -> None:
        id = len(self.todo_List) + 1
        field_val_zip = zip(self.fields, (id, priority, message, createdOn, None))
        csv_row = dict(field_val_zip)
        self.todo_List.append(csv_row)
        self.write_csvfile()

    def write_csvfile(self) -> None:
        with open(self.datafile, "w", newline="") as f:
            writer = csv.DictWriter(f, self.fields)
            writer.writeheader()
            writer.writerows(self.todo_List)  # pyright: ignore

    def Read(
        self, done: bool = False, priority: bool = False
    ) -> List[Dict[str, str | None | int]]:
        #
        # Logic flawed
        #
        new_list = []
        remove_completed = False
        if not done:  # remove the completedOn key from all dicts in list
            remove_completed = True

        for i, val in enumerate(self.todo_List):
            if (
                (priority and val["priority"] == 1)
                or (done and val["completedOn"] != "")
                or (not done and val["completedOn"] == "")
            ):
                new_list.append(val)
                if remove_completed:
                    del new_list[-1]["completedOn"]

        # if len(self.todo_List) == 0:
        #     return []
        # for i, val in enumerate(self.todo_List):
        #     if val["completedOn"] == "":  # not completed
        #         if done or (
        #             priority and val["priority"] == 0
        #         ):  # want completed or want priority
        #             del self.todo_List[i]
        #
        #     else:  # completed
        #         if priority and val["priority"] == 0:  # want priority
        #             del self.todo_List[i]

        return new_list

    def MarkDone(self, id: int, completedOn: str) -> int:
        try:
            if self.todo_List[id - 1]["completedOn"] != "":
                return 2
            else:
                self.todo_List[id - 1]["completedOn"] = completedOn
                self.write_csvfile()
                return 0
        except IndexError:
            return 1
