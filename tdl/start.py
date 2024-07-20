from .cmd_callback import *
from .cmdline import cmd_parser


def main():
    args = cmd_parser()
    if args.command == "add":
        add_item(args.message, args.priority)
    elif args.command == "ls":
        show_list(args.sort)
    elif args.command == "del":
        delete_item()
