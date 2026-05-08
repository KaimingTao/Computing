## argparse demo

This project now includes an `argparse` example that builds the parser itself
from a TOML file. The Python code keeps only a tiny bootstrap parser that reads
which TOML schema to load.

Run with the default schema:

```bash
python build_parser.py
```

Override values from the command line:

```bash
python build_parser.py --name Alice --count 3 --mode quiet
```

Load a different TOML parser schema:

```bash
python build_parser.py custom.toml
```

Show the built-in version flag:

```bash
python build_parser.py --version
```

The default schema file is `argparse.toml`:

```toml
[parser]
prog = "argparse-demo"
description = "Demo CLI built entirely from a TOML argparse schema."

[[arguments]]
flags = ["--version"]
action = "version"
version = "argparse-demo 1.0.0"

[[arguments]]
flags = ["--name"]
type = "str"
default = "TOML user"
help = "Name to greet."

[[arguments]]
flags = ["--count"]
type = "int"
default = 2
help = "How many greetings to print."

[[arguments]]
flags = ["--mode"]
choices = ["quiet", "normal", "debug"]
default = "debug"
help = "Output mode."

[[arguments]]
flags = ["--enabled"]
action = "BooleanOptionalAction"
default = true
help = "Enable or disable the demo feature."
```

Supported schema keys in `build_parser.py` currently include:

- `flags`
- `help`
- `default`
- `type`
- `choices`
- `action`
- `version`
- `nargs`
- `metavar`
- `dest`

## click demo

This project also includes a `click` version that builds the command from
`click.toml`.

Run with the default schema:

```bash
python build_parse_click.py
```

Override values from the command line:

```bash
python build_parse_click.py --name Alice --count 3 --mode quiet
```

Load a different TOML command schema:

```bash
python build_parse_click.py custom.toml
```

Show the built-in version flag:

```bash
python build_parse_click.py --version
```

| Tool       | Type             | Best for                   | Pros                                                                                     | Cons                                               | Use today?                |
| ---------- | ---------------- | -------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------- |
| `argparse` | Built-in         | Normal Python CLI scripts  | No install, supports positional args, optional args, flags, types, defaults, subcommands | Verbose for large apps                             | Yes, recommended standard |
| `optparse` | Built-in, old    | Maintaining legacy scripts | Simple, still works in old code                                                          | Deprecated, weak positional args, poor subcommands | No, only legacy           |
| `click`    | Third-party      | Professional CLI apps      | Clean decorators, great help text, nested commands, widely used                          | Extra dependency, framework style                  | Yes                       |
| `typer`    | Third-party      | Modern typed CLI apps      | Uses type hints, concise, good docs/help, built on Click                                 | Extra dependency, some magic                       | Yes                       |
| `docopt`   | Third-party      | Usage-text-first CLIs      | Parser comes from command usage documentation                                            | Less common, weaker validation                     | Sometimes                 |
| `sys.argv` | Built-in, manual | Very tiny scripts          | No library, direct access to raw args                                                    | No validation, no help text, hard to maintain      | Only tiny hacks           |



| Feature                         | `argparse` | `optparse` | `click`   | `typer`   | `docopt`        | `sys.argv` |
| ------------------------------- | ---------- | ---------- | --------- | --------- | --------------- | ---------- |
| Built in                        | Yes        | Yes        | No        | No        | No              | Yes        |
| Deprecated                      | No         | Yes        | No        | No        | No              | No         |
| Positional args                 | Good       | Weak       | Good      | Good      | Good            | Manual     |
| Optional args                   | Good       | Good       | Good      | Good      | Good            | Manual     |
| Boolean flags                   | Good       | Good       | Good      | Good      | Good            | Manual     |
| Subcommands                     | Good       | Poor       | Excellent | Excellent | Limited         | Manual     |
| Type conversion                 | Good       | Limited    | Good      | Excellent | Limited         | Manual     |
| Auto help text                  | Good       | Basic      | Excellent | Excellent | From usage text | No         |
| Best choice for beginners       | Good       | No         | Okay      | Good      | Okay            | No         |
| Best choice for serious CLI app | Okay       | No         | Excellent | Excellent | No              | No         |
