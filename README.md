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

data_dir = "~/.tdl" # todo list storage directory
backend = "sqlite" # | csv
```

## Development

1. Clone the repo and cd into it.
2. Have `uv` installed (Nix users can just `nix develop` to get a devShell with deps).
3. Run: `uv sync`.
4. Activate the venv.

### TODO

- [ ] Add option to delete done items.
- [ ] Pretty print the output with arrow.
