## Features

- Customizable with a Config file.
- Multiple storage backends.

## Usage

```sh
$ tdl -h
usage: tdl [-h] {add,ls,done} ...

Manage a todo-list

positional arguments:
  {add,ls,done}
    add          add item to list
    ls           list items
    done         Mark an item as completed

options:
  -h, --help     show this help message and exit
```

### Configuration

Some options can be set in a config file, which has the following defaults:

```toml
# ~/.tdl/.config.toml

data_dir = "~/.tdl" # ToDo List storage directory
backend = "sqlite" # | csv

# colors of the displayed table
# each entry is a string containing a rich' style definition
# see: https://rich.readthedocs.io/en/stable/style.html#defining-styles
[style]
# $field is one of (id, message, created_on, due_date, priority, completed_one)
title = "bold italic #C6A14D"
col_header = "bold blue" # default for all column headers
# col_header_$field = "" # override column header for specific field
col = "" # default for all columns
# col_$field = "" # override column for specific field
col_id = "bold blue"
row_priority_override = "bold red" # entire row style for priority entries

```

## Development

1. Clone the repo and cd into it.
2. Have `uv` installed (Nix users can just `nix develop` to get a devShell with deps).
3. Run: `uv sync`.
4. Activate the venv.

### TODO

- [ ] Add option to delete done items.
- [ ] Pretty print the output with arrow.
