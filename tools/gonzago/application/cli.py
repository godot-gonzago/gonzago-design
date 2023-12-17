from pathlib import Path

import typer
from rich.console import Console

from ..config import CONFIG, dst_path, src_path


APPLICATION_SRC = src_path("./engine/application")
APPLICATION_DST = dst_path("application")


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
