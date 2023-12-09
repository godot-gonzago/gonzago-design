from rich import print
from typing import Annotated, Optional
from gonzago import CONFIG_FILE_PATH, SOURCE_DIR_PATH, __app_name__, __version__, palettes, icons
import typer


app = typer.Typer()
app.add_typer(palettes.app, name="palettes")
app.add_typer(icons.app, name="icons")


@app.command("init")
def init() -> None:
    """
    Initialize Gonzago Design Tools.
    """
    print(CONFIG_FILE_PATH)
    print(SOURCE_DIR_PATH)


def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback(no_args_is_help=True)
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None
) -> None:
    """
    Gonzago Design Tools.

    Command line interface providing tools to automate Gonzago design asset production.
    """
    return


if __name__ == "__main__":
    app()
