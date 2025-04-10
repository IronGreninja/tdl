from dataclasses import asdict

import arrow
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .backend.models import ListEntry, fieldDisplayName, get_fields

console = Console()

default_style: dict[str, str] = {
    "title": "bold italic #C6A14D",
    "col_header": "bold blue",  # default for all column headers
    # "col_header_$field": "", # override col header for field
    **{f"col_header_{field}": "" for field in get_fields()},
    "col": "",  # default for all cols
    # "col_$field": "", # override col for field
    **{f"col_{field}": "" for field in get_fields()},
    "col_id": "bold blue",
    "row_priority_override": "bold red",
}


class DisplayList:
    def __init__(
        self,
        *,
        todoList: list[ListEntry],
        style: dict[str, str] | None = None,
        timestamp_format: str,
        humanize: bool = False,
    ):
        self.todoList = todoList
        if style:
            self.style = default_style | style  # Merge styles
        else:
            self.style = default_style

        self.timestamp_format = timestamp_format
        self.humanize = humanize

    def __call__(self) -> None:
        console.print(self.mkTable())

    def mkTable(self) -> Table:
        table = Table(
            title="ToDo List",
            title_style=self.style.get("title", ""),
            highlight=True,
            box=box.ROUNDED,
            # show_lines=True,
        )
        for field in get_fields():
            style = self.style.get(f"col_header_{field}") or self.style.get(
                "col_header", ""
            )
            table.add_column(
                Text(fieldDisplayName[field], style=style),
                justify="full",
                style=self.style.get("col"),
                no_wrap=True,
            )
        for entry in self.todoList:
            row_entries: list[Text] = []
            for col, val in asdict(entry).items():
                # Format timestamp
                if (
                    self.timestamp_format
                    and col in ("created_on", "due_date", "completed_on")
                    and val != ""
                ):
                    arw = arrow.get(val)
                    if col == "due_date" and self.humanize:
                        val = arw.humanize(arrow.now(), granularity=["day", "hour"])
                    else:
                        val = arw.format(self.timestamp_format)

                override_style = self.style["row_priority_override"]
                if entry.priority and override_style != "":
                    style = override_style
                else:
                    style = self.style[f"col_{col}"]
                row = Text(f"{val}", style=style)
                row_entries.append(row)
            table.add_row(*row_entries)
        return table


if __name__ == "__main__":
    pass
