import typer

from .create import create
from .import_palette import import_palette
from .list_palettes import list_palettes
from .list_readers import list_readers
from .list_writers import list_writers
from .publish import publish

palettes_app = typer.Typer()

palettes_app.command("create")(create)
palettes_app.command("import")(import_palette)
palettes_app.command("list")(list_palettes)
palettes_app.command("readers")(list_readers)
palettes_app.command("writers")(list_writers)
palettes_app.command("publish")(publish)


@palettes_app.callback(no_args_is_help=True)
def palettes_callback() -> None:
    """
    Color palette tools.
    """
    pass
