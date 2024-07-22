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
        help="set item priority. [1: lowest, 3: highest] (default: 1)",
        type=int,
        default=1,
        choices=[1, 2, 3],
        dest="priority",
    )

    parser_show = cmd_subparser.add_parser("ls", help="list items")
    parser_show.add_argument(
        "-s",
        help="Sort the display {d: date, p: priority} (default: p)",
        type=str,
        choices=["d", "p"],
        default="p",
        metavar="{d,p}",
        dest="sort",
    )

    # TODO: add delete sub-command
    parser_delete = cmd_subparser.add_parser("del", help="delete an item from list")

    args = parser.parse_args(
        # show help when used without any arguments
        args=None if sys.argv[1:] else ["--help"]
    )
    return args


if __name__ == "__main__":
    args = cmd_parser()
    print(args)
