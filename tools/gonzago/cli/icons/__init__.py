import typer

from .list import list
from .publish import publish

icons_app = typer.Typer()

icons_app.command("list")(list)
icons_app.command("publish")(publish)


@icons_app.callback(no_args_is_help=True)
def icons_callback() -> None:
    """
    Editor icon tools.
    """
