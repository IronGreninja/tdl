from dataclasses import dataclass

fields = ("id", "message", "created_on", "due_date", "priority", "completed_on")


@dataclass
class ListEntry:
    message: str
    created_on: str
    due_date: str
    priority: bool
    completed_on: str


@dataclass
class ListEntry_R(ListEntry):
    id: int
