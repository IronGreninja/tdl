# ToDo List cli

Basic aah cli app with python, built for practice.

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

### Development

1. Clone the repo and cd into it.
2. Create a venv and enter it: `python -m venv .venv && source .venv/bin/activate`. This project is a flake so nix users can instead just do: `nix develop`(ensures venv and enters it).
3. Do an editable install: `pip install -e .`

### Install

#### NixOS

[Example Derivation](./nix/build.nix). Change `src` to `fetchFromGitHub` this repo and include it in system/home packages.

### ToDo

- [ ] Add option to delete done items
