from pathlib import Path

import typer
from rich.console import Console

from ..config import CONFIG


APPLICATION_SOURCE_DIR: Path = Path(CONFIG["paths"]["src"]).joinpath("./engine/application").resolve()
APPLICATION_DST_DIR: Path = Path(CONFIG["paths"]["dst"]).joinpath("application").resolve()


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
