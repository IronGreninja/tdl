from .cmdline import cmd_parser
from .tdl import TDL


def main():
    args = cmd_parser()
    tdl = TDL()
    if args.command == "add":
        tdl.add_item(message=args.message, priority=args.priority)
    elif args.command == "ls":
        tdl.show_list(sort_by=args.sort_by)
    elif args.command == "del":
        tdl.delete_item(sort_by=args.sort_by)
