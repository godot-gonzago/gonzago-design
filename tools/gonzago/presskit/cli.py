from pathlib import Path

import typer
from rich.console import Console

from ..config import CONFIG


PRESSKIT_SOURCE_DIR: Path = Path(CONFIG["paths"]["src"]).joinpath("./engine/presskit").resolve()
PRESSKIT_DST_DIR: Path = Path(CONFIG["paths"]["dst"]).joinpath("presskit").resolve()


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
    Presskit tools.
    """


if __name__ == "__main__":
    app()
