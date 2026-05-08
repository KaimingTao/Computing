from __future__ import annotations

from pathlib import Path
import sys
import tomllib

import click


DEFAULT_CONFIG_PATH = Path("click.toml")
TYPE_MAP = {
    "str": click.STRING,
    "int": click.INT,
    "float": click.FLOAT,
    "path": click.Path(path_type=Path),
}


def load_command_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Click config not found: {path}")

    with path.open("rb") as file:
        return tomllib.load(file)


def build_command(config: dict) -> click.Command:
    command_config = config.get("command", {})

    def callback(**kwargs: object) -> None:
        run_demo(kwargs)

    command = click.command(
        name=command_config.get("prog", "toml-click-demo"),
        help=command_config.get("description"),
    )(callback)

    for option_config in reversed(config.get("options", [])):
        param_decls = option_config["flags"]
        kwargs: dict[str, object] = {
            "help": option_config.get("help"),
            "default": option_config.get("default"),
            "show_default": option_config.get("show_default", True),
        }

        option_type = option_config.get("type")
        if option_type:
            kwargs["type"] = TYPE_MAP[option_type]

        choices = option_config.get("choices")
        if choices:
            kwargs["type"] = click.Choice(choices)

        is_flag = option_config.get("is_flag", False)
        if is_flag:
            kwargs["is_flag"] = True
            kwargs["default"] = option_config.get("default", False)

        count = option_config.get("count", False)
        if count:
            kwargs["count"] = True

        version = option_config.get("version")
        if version:
            def show_version(
                ctx: click.Context,
                param: click.Parameter,
                value: bool,
                *,
                version_text: str = version,
            ) -> None:
                del param
                if not value or ctx.resilient_parsing:
                    return
                click.echo(version_text)
                ctx.exit()

            kwargs["is_flag"] = True
            kwargs["is_eager"] = True
            kwargs["expose_value"] = False
            kwargs["callback"] = show_version

        command = click.option(*param_decls, **kwargs)(command)

    return command


def parse_invocation_args(argv: list[str]) -> tuple[Path, list[str]]:
    if argv and not argv[0].startswith("-"):
        return Path(argv[0]), argv[1:]

    return DEFAULT_CONFIG_PATH, argv


def run_demo(values: dict[str, object]) -> None:
    print("Loaded options:")
    for key, value in values.items():
        print(f"  {key:<7} = {value}")

    if not {"name", "count", "mode", "enabled"}.issubset(values):
        return

    if not values["enabled"]:
        print("Feature disabled.")
        return

    name = str(values["name"])
    count = int(values["count"])
    mode = str(values["mode"])

    for index in range(1, count + 1):
        if mode == "quiet":
            print(name)
        elif mode == "debug":
            print(f"[{index}/{count}] Hello, {name}!")
        else:
            print(f"Hello, {name}!")


def main() -> None:
    config_path, cli_args = parse_invocation_args(sys.argv[1:])
    config = load_command_config(config_path)
    command = build_command(config)
    if not any(arg == "--version" for arg in cli_args):
        print(f"Parser config: {config_path}")
    command.main(args=cli_args, standalone_mode=False)


if __name__ == "__main__":
    main()
