from pathlib import Path

import typer
from rich.console import Console

from .. import BASE_DIR_PATH, SOURCE_DIR_PATH


APPLICATION_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./engine/application").resolve()
APPLICATION_DST_DIR: Path = BASE_DIR_PATH.joinpath("application").resolve()


app = typer.Typer()
console: Console = Console()


@app.command("publish")
def publish():
    """
    Build optimized icons.
    """
    pass


@app.command("readme")
def build_readme():
    pass


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Application asset tools.
    """


if __name__ == "__main__":
    app()
