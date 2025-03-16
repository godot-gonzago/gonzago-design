import typer
from rich.console import Console

from ..config import CONFIG

APPLICATION_SRC = CONFIG.src_path("./engine/application")
APPLICATION_DST = CONFIG.dst_path("application")


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
