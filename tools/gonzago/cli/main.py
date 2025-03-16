from typing import Annotated, Optional

import typer
from rich.console import Console

from gonzago import __app_name__, __version__
from gonzago.core.config import CONFIG

from .application import application_app
from .assets import assets_app
from .icons import icons_app
from .palettes import palettes_app
from .presskit import presskit_app

app = typer.Typer()
console: Console = Console()

app.add_typer(application_app, name="application")
app.add_typer(assets_app, name="assets")
app.add_typer(icons_app, name="icons")
app.add_typer(palettes_app, name="palettes")
app.add_typer(presskit_app, name="presskit")


@app.command("uninit")
def uninit() -> None:
    """
    Uninitialize Gonzago Design Tools.
    """
    CONFIG.clear_yaml()


@app.command("open_config")
def open_config() -> None:
    """
    Open Gonzago Design Tools config.
    """
    # https://typer.tiangolo.com/tutorial/launch/
    file = CONFIG.get_yaml_file_location()
    if not file.exists():
        console.print(f"'{file.as_posix()}' does not exist!")
        typer.Abort()
        return
    console.print(f"Opening '{file.as_posix()}'")
    typer.launch(str(file), locate=True)


@app.command("init")
def init() -> None:
    """
    Initialize Gonzago Design Tools.
    """
    file = CONFIG.get_yaml_file_location()
    if file.exists() and not typer.confirm(
        f"'{file.as_posix()}' already exists. Do you wish to override it?"
    ):
        return
    CONFIG.save_to_yaml()
    console.print(f"Saved config under '{file.as_posix()}'")


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"{__app_name__} v{__version__}")
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
    ] = None,
) -> None:
    """
    Gonzago Design Tools.

    Command line interface providing tools to automate Gonzago design asset production.
    """
    # TODO: Check if config exists otherwise force init?
    return


if __name__ == "__main__":
    app()
