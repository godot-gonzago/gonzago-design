from pathlib import Path

import typer
from rich.console import Console

from ..config import CONFIG, dst_path, src_path


ASSETS_SRC: Path = src_path("./assets")
ASSETS_DST: Path = dst_path("assets")


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
    Tool and demo asset tools.
    """


if __name__ == "__main__":
    app()
