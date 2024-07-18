import csv
import sys
from pathlib import Path
from platform import system


def append_item(msg: str, P: int):
    data_dir = get_tdl_data_dir()
    list_file = data_dir / "default-list.csv"
    if not list_file.exists():
        return (1, f"Default todolist file ({str(list_file)}) does not exist")


def show_list(sort: str):
    pass


def delete_item():
    pass


def get_tdl_data_dir():
    P = system()
    if P == "Linux":
        data_dir = Path.home() / ".tdl"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    elif P == "Windows":  # TODO:
        print(P, "is not supported")
        sys.exit(1)
