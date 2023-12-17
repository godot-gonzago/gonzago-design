from pathlib import Path
from rich import print
from typing import Annotated, Optional
import typer

from .config import CONFIG, CONFIG_FILE, clear, save
from . import (
    __app_name__,
    __version__,
    application,
    assets,
    icons,
    palettes,
    presskit,
)


app = typer.Typer()
app.add_typer(application.app, name="application")
app.add_typer(assets.app, name="assets")
app.add_typer(icons.app, name="icons")
app.add_typer(palettes.app, name="palettes")
app.add_typer(presskit.app, name="presskit")


@app.command("uninit")
def uninit() -> None:
    """
    Uninitialize Gonzago Design Tools.
    """
    clear()


@app.command("open_config")
def open_config() -> None:
    """
    Open Gonzago Design Tools config.
    """
    if not CONFIG_FILE.is_file():
        print("Config does not exist!")
        typer.Abort()
        return
    print(f"Opening {CONFIG_FILE.as_posix()}")
    typer.launch(str(CONFIG_FILE), locate=True)


@app.command("init")
def init() -> None:
    """
    Initialize Gonzago Design Tools.
    """
    src: str = CONFIG["paths"]["src"]
    if not src or not typer.confirm(f"Source files path already set to '{src}'.\nDo you wish to keep it?"):
        CONFIG["paths"]["src"] = typer.prompt("Source files path")

    dst: str = CONFIG["paths"]["dst"]
    if not dst or not typer.confirm(f"Output files path already set to '{dst}'.\nDo you wish to keep it?"):
        CONFIG["paths"]["dst"] = typer.prompt("Output files path")

    inkscape: str = CONFIG["inkscape"]["path"]
    if not inkscape or not typer.confirm(f"Inkscape path already set to '{inkscape}'.\nDo you wish to keep it?"):
        CONFIG["inkscape"]["path"] = typer.prompt("Inkscape path")

    blender: str = CONFIG["blender"]["path"]
    if not blender or not typer.confirm(f"Blender path already set to '{blender}'.\nDo you wish to keep it?"):
        CONFIG["blender"]["path"] = typer.prompt("Blender path")

    save(CONFIG)


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
    # TODO: Check if config exists otherwise force init?
    return


if __name__ == "__main__":
    app()
