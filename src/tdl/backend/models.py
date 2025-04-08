from dataclasses import dataclass, fields


@dataclass
class ListEntry:
    id: int | None
    message: str
    created_on: str
    due_date: str
    priority: bool
    completed_on: str


fieldDisplayName: dict[str, str] = {
    "id": "ID",
    "message": "Message",
    "created_on": "Created On",
    "due_date": "Due Date",
    "priority": "Priority",
    "completed_on": "Completed On",
}


def get_fields():
    _fields = tuple(f.name for f in fields(ListEntry))
    return _fields


def get_Q_fields() -> tuple[str, int]:
    _fields = get_fields()
    _Qfields = ",".join(_fields)
    return (_Qfields, len(_fields))
