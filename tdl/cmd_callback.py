import csv
import sys
from pathlib import Path
from platform import system

TDL_DATA_DIR = Path.home() / ".tdl"
TDL_DATA_FILE = TDL_DATA_DIR / "list.csv"
TDL_LIST_FIELDS = ["priority", "message"]


def add_item(msg: str, P: int):

    F = TDL_LIST_FIELDS
    mode = "a"
    if not TDL_DATA_DIR.exists():
        TDL_DATA_DIR.mkdir()
    if not TDL_DATA_FILE.exists():
        TDL_DATA_FILE.touch()
        print(f"Created default list in {TDL_DATA_FILE}")
        mode = "w"
    try:
        with open(TDL_DATA_FILE, mode, newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=F)
            if mode == "w":
                writer.writeheader()
            writer.writerow({F[0]: P, F[1]: msg})
    except:
        print("Error ocurred while writing record!")
        sys.exit(1)


def show_list(sort_by: str):

    if not TDL_DATA_FILE.exists():
        print("List empty")
        return
    try:
        with open(TDL_DATA_FILE, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            tdl_items = list(reader)
            if sort_by == "p":
                tdl_items.sort(reverse=True, key=lambda item: item["priority"])
            # TODO: implement sort by date
            print("\t".join(TDL_LIST_FIELDS))
            for item in tdl_items:
                for field in item.values():
                    print(field, end="\t")
                print()
    except:
        print("Error ocurred while reading records!")
        sys.exit(1)


def delete_item():

    F = TDL_LIST_FIELDS
    # read list contents
    if not TDL_DATA_FILE.exists():
        print("List empty")
        return
    try:
        with open(TDL_DATA_FILE, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            tdl_items = list(reader)
    except:
        print("Error reading list!")
        sys.exit(1)

    if len(tdl_items) == 0:
        print("List empty")
        return

    # print them with index
    print("\t".join(F))
    for index, item in enumerate(tdl_items):
        print(f"{index}) ", end="")
        for field in item.values():
            print(field, end="\t")
        print()

    print(
        "Enter index number(s) separated with a space to delete(empty to cancel): ",
        end="",
    )
    inp = input()

    # delete indexes and writeback
    if inp == "":
        return
    indexes = list(map(int, inp.split()))
    for i in sorted(indexes, reverse=True):
        if 0 <= i and i <= len(tdl_items) - 1:
            del tdl_items[i]
        else:
            print("Invalid index(es) encountered. Aborting")
            sys.exit(1)

    try:
        with open(TDL_DATA_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(F)
            for item in tdl_items:
                writer.writerow(item.values())
    except:
        print("Error writing back!")
        sys.exit(1)
