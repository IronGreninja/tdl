import sys
from argparse import ArgumentParser

from .tdl import TDL


def mkParser() -> ArgumentParser:
    """
    Parse and return command line arguments
    """
    # create the top-level parser
    parser = ArgumentParser(
        prog="tdl",
        description="Manage a todo-list",
    )
    # command subparser
    cmd_subparser = parser.add_subparsers(required=True, prog="", dest="command")

    # create the parsers for sub-command
    parser_add = cmd_subparser.add_parser("do", help="add item to list")
    parser_add.add_argument(
        "-m", help="item message", metavar="MSG", required=True, dest="message"
    )
    parser_add.add_argument(
        "-p",
        help="Mark this item as important (higher priority)",
        action="store_true",
        dest="priority",
    )
    parser_add.add_argument(
        "-d",
        help="""
            Set due date relative to now.
            Ex - '2d', '3h', '2d3h'
            (d = days, h = hours)
        """,
        action="store",
        dest="due_date",
    )

    parser_show = cmd_subparser.add_parser("ls", help="list items")
    group = parser_show.add_mutually_exclusive_group()
    group.add_argument(
        "-p", help="Show only priority items", action="store_true", dest="priority"
    )
    group.add_argument(
        "-c", help="show only completed items", action="store_true", dest="done"
    )
    group.add_argument("-a", help="show all items", action="store_true", dest="all")

    parser_done = cmd_subparser.add_parser("done", help="Mark an item as completed")
    parser_done.add_argument(
        "-i", help="ID to mark", required=True, type=int, dest="id"
    )

    cmd_subparser.add_parser("clear", help="clear all completed items")

    return parser


def start():
    args = mkParser().parse_args(
        # show help when used without any arguments
        args=None if sys.argv[1:] else ["--help"]
        # ["--help"]
    )
    TDL(args)()


if __name__ == "__main__":
    args = mkParser().parse_args()
    print(args)
