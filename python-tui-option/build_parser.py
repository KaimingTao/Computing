from __future__ import annotations

import argparse
from pathlib import Path
import tomllib


DEFAULT_CONFIG_PATH = Path("argparse.toml")
TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "path": Path,
}
ACTION_MAP = {
    "store_true": "store_true",
    "store_false": "store_false",
    "append": "append",
    "count": "count",
    "version": "version",
    "BooleanOptionalAction": argparse.BooleanOptionalAction,
}


def load_parser_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Parser config not found: {path}")

    with path.open("rb") as file:
        return tomllib.load(file)


def build_parser(config: dict) -> argparse.ArgumentParser:
    parser_config = config.get("parser", {})
    parser = argparse.ArgumentParser(
        prog=parser_config.get("prog", "toml-argparse-demo"),
        description=parser_config.get("description"),
    )

    for argument in config.get("arguments", []):
        flags = argument["flags"]
        kwargs = {}

        if "help" in argument:
            kwargs["help"] = argument["help"]
        if "default" in argument:
            kwargs["default"] = argument["default"]
        if "choices" in argument:
            kwargs["choices"] = argument["choices"]
        if "nargs" in argument:
            kwargs["nargs"] = argument["nargs"]
        if "metavar" in argument:
            kwargs["metavar"] = argument["metavar"]
        if "dest" in argument:
            kwargs["dest"] = argument["dest"]

        arg_type = argument.get("type")
        if arg_type:
            kwargs["type"] = TYPE_MAP[arg_type]

        action = argument.get("action")
        if action:
            kwargs["action"] = ACTION_MAP[action]

        if action == "version":
            kwargs["version"] = argument["version"]

        parser.add_argument(*flags, **kwargs)

    return parser


def parse_args() -> tuple[argparse.Namespace, Path]:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "parser_config",
        nargs="?",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
    )
    known_args, remaining_args = pre_parser.parse_known_args()

    config_path = known_args.parser_config
    config = load_parser_config(config_path)
    parser = build_parser(config)
    return parser.parse_args(remaining_args), config_path


def run_demo(args: argparse.Namespace) -> None:
    values = vars(args)

    print("Loaded options:")
    for key, value in values.items():
        print(f"  {key:<7} = {value}")

    if not {"name", "count", "mode", "enabled"}.issubset(values):
        return

    if not args.enabled:
        print("Feature disabled.")
        return

    for index in range(1, args.count + 1):
        if args.mode == "quiet":
            print(args.name)
        elif args.mode == "debug":
            print(f"[{index}/{args.count}] Hello, {args.name}!")
        else:
            print(f"Hello, {args.name}!")


def main() -> None:
    args, config_path = parse_args()
    print(f"Parser config: {config_path}")
    run_demo(args)


if __name__ == "__main__":
    main()
