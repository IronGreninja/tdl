from .cmdline import cmd_parser
from .tdl import TDL


def main():
    args = cmd_parser()
    tdl = TDL()
    if args.command == "add":
        tdl.add_item(message=args.message, priority=args.priority)
    elif args.command == "ls":
        tdl.show_list(priority=args.priority, showAll=args.showAll)
    elif args.command == "done":
        tdl.mark_done_item(id=args.ID)
