import sys
from argparse import ArgumentParser


def cmd_parser():
    # create the top-level parser
    parser = ArgumentParser(
        prog="tdl",
        description="Manage a todo-list",
    )
    # command subparser
    cmd_subparser = parser.add_subparsers(required=True, prog="", dest="command")

    # create the parsers for sub-command
    parser_add = cmd_subparser.add_parser("add", help="add item to list")
    parser_add.add_argument(
        "-m", help="item message", metavar="MSG", required=True, dest="message"
    )
    parser_add.add_argument(
        "-p",
        help="Mark this item as important (higher priority)",
        action="store_true",
        dest="priority",
    )

    parser_show = cmd_subparser.add_parser("ls", help="list items")
    parser_show.add_argument(
        "-p",
        help="Show only priority items",
        action="store_true",
        dest="priority",
    )
    parser_show.add_argument(
        "-a", help="Also show completed items", action="store_true", dest="showAll"
    )

    parser_done = cmd_subparser.add_parser("done", help="Mark an item as completed")
    parser_done.add_argument(
        "-i", help="ID to mark", required=True, type=int, dest="ID"
    )

    args = parser.parse_args(
        # show help when used without any arguments
        args=None if sys.argv[1:] else ["--help"]
    )
    return args


if __name__ == "__main__":
    args = cmd_parser()
    print(args)
