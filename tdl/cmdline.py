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
        help="set item priority. {1: lowest, 3: highest} (default: 1)",
        type=int,
        default=1,
        choices=(1, 2, 3),
        dest="priority",
    )

    parser_show = cmd_subparser.add_parser("ls", help="list items")
    parser_show.add_argument(
        "-s",
        help="Sort the display {o: oldest first, n: newest first, p: priority} (default: o)",
        type=str,
        choices=("o", "n", "p"),
        default="o",
        metavar="{o,n,p}",
        dest="sort_by",
    )

    parser_delete = cmd_subparser.add_parser("del", help="delete an item from list")
    # FIX: duplicate subparser argument '-s'
    parser_delete.add_argument(
        "-s",
        help="Sort the display {o: oldest first, n: newest first, p: priority} (default: o)",
        type=str,
        choices=("o", "n", "p"),
        default="o",
        metavar="{o,n,p}",
        dest="sort_by",
    )

    args = parser.parse_args(
        # show help when used without any arguments
        args=None if sys.argv[1:] else ["--help"]
    )
    return args


if __name__ == "__main__":
    args = cmd_parser()
    print(args)
